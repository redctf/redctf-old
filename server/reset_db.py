# Hack to use django app models in standalone script
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "redctf.settings")
django.setup()

# Imports
import argparse, contextlib, uuid
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from redctf.settings import RDB_HOST, RDB_PORT, CTF_DB, DATABASES
from users.models import User
from teams.models import Team
from users.validators import validate_username, validate_password, validate_email

def resetRethinkDB():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db_drop(CTF_DB).run(connection)
    except RqlRuntimeError:
        pass

    try:
        r.db_create(CTF_DB).run(connection)
        r.db(CTF_DB).table_create('challenges').run(connection)
        r.db(CTF_DB).table_create('categories').run(connection)
        r.db(CTF_DB).table_create('teams').run(connection)
        print('Realtime database setup complete')
    except RqlRuntimeError as e:
        print('Error during database setup: %s' % (e))
    finally:
        connection.close()


def resetDjangoDB(admin_name, admin_email, admin_password):
    # Remove database file if exists
    with contextlib.suppress(FileNotFoundError):
        os.remove(DATABASES['default']['NAME'])
    
    # Remove migrations
    os.system('find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')
    os.system('find . -path "*/migrations/*.pyc"  -delete')

    # Rebuild database
    os.system('python3 manage.py makemigrations')
    os.system('python3 manage.py migrate')   

    # Validate admin user command line arguments
    validate_username(admin_name)
    validate_email(admin_email)
    validate_password(admin_password)

    # Create team for admin user
    token = str(uuid.uuid4())
    admin_team = Team(name=admin_name, token=token)
    admin_team.save()

    # Create admin user assign admin team
    admin = User.objects.create_superuser(admin_name, admin_email, admin_password)
    admin.team = admin_team
    admin.save()

    # Push admin team to rethinkdb database
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db(CTF_DB).table('teams').insert({ 'sid': admin.team.id, 'name': admin.team.name, 'points': admin.team.points, 'correct_flags': admin.team.correct_flags, 'wrong_flags': admin.team.wrong_flags, 'solved': list(admin.team.solved.all().values_list('id', flat=True))}).run(connection)
    except RqlRuntimeError as e:
        raise Exception('Error adding admin team to realtime database: %s' % (e))
    finally:
        connection.close()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Redctf database reset script')
    parser.add_argument('--name', action="store", dest="admin_name", help='Username of admin user', default="admin")
    parser.add_argument('--email', action="store", dest="admin_email", help='Email of admin user', default="admin@redctf.com")
    parser.add_argument('--password', action="store", dest="admin_password", help='Password of admin user', default="Password123!")

    args = parser.parse_args()

    resetRethinkDB()
    resetDjangoDB(args.admin_name, args.admin_email, args.admin_password)
    
    