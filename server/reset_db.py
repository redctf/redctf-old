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
    
def insertCategories():
    # Push test categories to rethinkdb database
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db(CTF_DB).table('categories').insert({ 'id': "0229d0d6-c866-4bba-8631-4e9e79bab490", 'name': 'Web', 'sid': 1}).run(connection)
        r.db(CTF_DB).table('categories').insert({ 'id': "0229d0d6-c866-4bba-8631-4e9e39bab490", 'name': 'Forensics', 'sid': 2}).run(connection)
        r.db(CTF_DB).table('categories').insert({ 'id': "0229d0d6-c866-4bba-8631-4e9e79bab450", 'name': 'Miscellaneous', 'sid': 3}).run(connection)
        r.db(CTF_DB).table('categories').insert({ 'id': "0229d0d6-c866-4bba-8631-4e9e79bab491", 'name': 'Pwn', 'sid': 4}).run(connection)
        r.db(CTF_DB).table('categories').insert({ 'id': "0229d0d6-c166-4bba-8631-4e9e79bab491", 'name': 'Crypto', 'sid': 5}).run(connection)
    except RqlRuntimeError as e:
        raise Exception('Error adding categories to realtime database: %s' % (e))
    finally:
        connection.close()

def insertChallengeBoard():
    # Push test challenges to rethinkdb database
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db(CTF_DB).table('challenges').insert({ 'category': 1, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab410", 'points': 100, 'sid': 1, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 1, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab411", 'points': 200, 'sid': 2, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 1, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab412", 'points': 300, 'sid': 3, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 1, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab413", 'points': 400, 'sid': 4, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 1, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab414", 'points': 500, 'sid': 5, 'title': 'Test Title'}).run(connection)

        r.db(CTF_DB).table('challenges').insert({ 'category': 2, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab420", 'points': 100, 'sid': 6, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 2, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab421", 'points': 200, 'sid': 7, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 2, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab422", 'points': 300, 'sid': 8, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 2, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab423", 'points': 400, 'sid': 9, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 2, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab424", 'points': 500, 'sid': 10, 'title': 'Test Title'}).run(connection)

        r.db(CTF_DB).table('challenges').insert({ 'category': 3, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab430", 'points': 100, 'sid': 11, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 3, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab431", 'points': 200, 'sid': 12, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 3, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab432", 'points': 300, 'sid': 13, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 3, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab433", 'points': 400, 'sid': 14, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 3, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab434", 'points': 500, 'sid': 15, 'title': 'Test Title'}).run(connection)

        r.db(CTF_DB).table('challenges').insert({ 'category': 4, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab440", 'points': 100, 'sid': 16, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 4, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab441", 'points': 200, 'sid': 17, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 4, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab442", 'points': 300, 'sid': 18, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 4, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab443", 'points': 400, 'sid': 19, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 4, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab444", 'points': 500, 'sid': 20, 'title': 'Test Title'}).run(connection)

        r.db(CTF_DB).table('challenges').insert({ 'category': 5, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab450", 'points': 100, 'sid': 21, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 5, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab451", 'points': 200, 'sid': 22, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 5, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab452", 'points': 300, 'sid': 23, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 5, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab453", 'points': 400, 'sid': 24, 'title': 'Test Title'}).run(connection)
        r.db(CTF_DB).table('challenges').insert({ 'category': 5, 'description': 'Test Description', 'id': "0229d0d6-c166-4bba-8631-4e9e79bab454", 'points': 500, 'sid': 25, 'title': 'Test Title'}).run(connection)
    except RqlRuntimeError as e:
        raise Exception('Error adding challenges to realtime database: %s' % (e))
    finally:
        connection.close()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Redctf database reset script')
    parser.add_argument('--name', action="store", dest="admin_name", help='Username of admin user', default="admin")
    parser.add_argument('--email', action="store", dest="admin_email", help='Email of admin user', default="admin@redctf.com")
    parser.add_argument('--password', action="store", dest="admin_password", help='Password of admin user', default="Password123!")
    parser.add_argument('--cats', action="store_true", dest="cats", help='Insert Test Categories')
    parser.add_argument('--chals', action="store_true", dest="chals", help='Insert Test Challenges')

    args = parser.parse_args()

    resetRethinkDB()
    resetDjangoDB(args.admin_name, args.admin_email, args.admin_password)

    if args.cats:
        insertCategories()

    if args.chals:
        insertChallengeBoard()

    
    