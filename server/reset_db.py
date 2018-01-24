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
from categories.models import Category
from challenges.models import Challenge
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


def resetDjangoDB():
    # Remove database file if exists
    with contextlib.suppress(FileNotFoundError):
        os.remove(DATABASES['default']['NAME'])
    
    # Remove migrations
    os.system('find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')
    os.system('find . -path "*/migrations/*.pyc"  -delete')

    # Rebuild database
    os.system('python3 manage.py makemigrations')
    os.system('python3 manage.py migrate')   

    
def makeAdminUser(admin_name, admin_email, admin_password):
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
    # Save the category
    web = Category(name="Web")
    web.save()
    forensics = Category(name="Forensics")
    forensics.save()
    miscellaneous = Category(name="Miscellaneous")
    miscellaneous.save()
    pwn = Category(name="Pwn")
    pwn.save()
    crypto = Category(name="Crypto")
    crypto.save()

    # Push test categories to rethinkdb database
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db(CTF_DB).table('categories').insert({'sid': web.id, 'name': web.name, 'id': web.id }).run(connection)
        r.db(CTF_DB).table('categories').insert({'sid': forensics.id, 'name': forensics.name, 'id': forensics.id }).run(connection)
        r.db(CTF_DB).table('categories').insert({'sid': miscellaneous.id, 'name': miscellaneous.name, 'id': miscellaneous.id }).run(connection)
        r.db(CTF_DB).table('categories').insert({'sid': pwn.id, 'name': pwn.name, 'id': pwn.id }).run(connection)
        r.db(CTF_DB).table('categories').insert({'sid': crypto.id, 'name': crypto.name, 'id': crypto.id }).run(connection)
    except RqlRuntimeError as e:
        raise Exception('Error adding categories to realtime database: %s' % (e))
    finally:
        connection.close()

def insertChallengeBoard():
    i = 1
    # Push test challenges to rethinkdb database
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        for category in Category.objects.all():
            # Save the challenge flag to the database
            challenge_100 = Challenge(category=category, flag="flag{0}".format(i), points=100)
            challenge_100.save()
            i+=1

            # Save the challenge flag to the database
            challenge_200 = Challenge(category=category, flag="flag{0}".format(i), points=200)
            challenge_200.save()
            i+=1

            # Save the challenge flag to the database
            challenge_300 = Challenge(category=category, flag="flag{0}".format(i), points=300)
            challenge_300.save()
            i+=1

            # Save the challenge flag to the database
            challenge_400 = Challenge(category=category, flag="flag{0}".format(i), points=400)
            challenge_400.save()
            i+=1

            # Save the challenge flag to the database
            challenge_500 = Challenge(category=category, flag="flag{0}".format(i), points=500)
            challenge_500.save()
            i+=1

            r.db(CTF_DB).table('challenges').insert({ 'sid': challenge_100.id, 'category': challenge_100.category.id, 'title': 'Test Title', 'points': challenge_100.points, 'description': 'Test Description', 'id': challenge_100.id }).run(connection)
            r.db(CTF_DB).table('challenges').insert({ 'sid': challenge_200.id, 'category': challenge_200.category.id, 'title': 'Test Title', 'points': challenge_200.points, 'description': 'Test Description', 'id': challenge_200.id }).run(connection)
            r.db(CTF_DB).table('challenges').insert({ 'sid': challenge_300.id, 'category': challenge_300.category.id, 'title': 'Test Title', 'points': challenge_300.points, 'description': 'Test Description', 'id': challenge_300.id }).run(connection)
            r.db(CTF_DB).table('challenges').insert({ 'sid': challenge_400.id, 'category': challenge_400.category.id, 'title': 'Test Title', 'points': challenge_400.points, 'description': 'Test Description', 'id': challenge_400.id }).run(connection)
            r.db(CTF_DB).table('challenges').insert({ 'sid': challenge_500.id, 'category': challenge_500.category.id, 'title': 'Test Title', 'points': challenge_500.points, 'description': 'Test Description', 'id': challenge_500.id }).run(connection)


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
    resetDjangoDB()
    makeAdminUser(args.admin_name, args.admin_email, args.admin_password)
    makeAdminUser('team2', 'team2@gmail.com', 'Password123!')
    makeAdminUser('team3', 'team3@gmail.com', 'Password123!')
    makeAdminUser('team4', 'team4@gmail.com', 'Password123!')
    makeAdminUser('team5', 'team5@gmail.com', 'Password123!')

    if args.cats:
        insertCategories()

    if args.chals:
        insertChallengeBoard()

    
    