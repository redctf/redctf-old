# Hack to use django app models in standalone script
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "redctf.settings")
django.setup()

# Imports
import argparse, contextlib, uuid
import json
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from django.utils.dateformat import format
from django.utils import timezone
from datetime import timedelta
from redctf.settings import RDB_HOST, RDB_PORT, CTF_DB, DATABASES
from users.models import User
from teams.models import Team
from categories.models import Category
from challenges.models import Challenge
from ctfs.models import Ctf
from containers.models import Container
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
        r.db(CTF_DB).table_create('ctfs').run(connection)
        r.db(CTF_DB).table_create('containers').run(connection)
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

    
def makeAdminUser(admin_name, admin_email, admin_password, hidden):
    # Validate admin user command line arguments
    validate_username(admin_name)
    validate_email(admin_email)
    validate_password(admin_password)

    # Create team for admin user
    token = str(uuid.uuid4())
    while Team.objects.filter(token__iexact=token).exists():
        token = str(uuid.uuid4())
    admin_team = Team(name=admin_name, token=token, hidden=hidden)
    admin_team.save()

    # Create admin user assign admin team
    admin = User.objects.create_superuser(admin_name, admin_email, admin_password)
    admin.team = admin_team
    admin.save()

    # Push admin team to rethinkdb database
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db(CTF_DB).table('teams').insert({ 'sid': admin.team.id, 'name': admin.team.name, 'points': admin.team.points, 'hidden': hidden, 'correct_flags': admin.team.correct_flags, 'wrong_flags': admin.team.wrong_flags, 'solved': [], 'created': format(admin.team.created, 'U')}).run(connection)
    except RqlRuntimeError as e:
        raise Exception('Error adding admin team to realtime database: %s' % (e))
    finally:
        connection.close()

def makeUser(user_name, user_email, user_password, hidden):
    # Validate admin user command line arguments
    validate_username(user_name)
    validate_email(user_email)
    validate_password(user_password)

    # Create team for admin user
    token = str(uuid.uuid4())
    while Team.objects.filter(token__iexact=token).exists():
        token = str(uuid.uuid4())

    user_team = Team(name=user_name, token=token, hidden=hidden)
    user_team.save()

    user = User(
            username=user_name,
            email=user_email,
            team=user_team,
            hidden=hidden
        )
    user.set_password(user_password)
    user.save()

    # Push admin team to rethinkdb database
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db(CTF_DB).table('teams').insert({ 'sid': user.team.id, 'name': user.team.name, 'points': user.team.points, 'hidden': hidden, 'correct_flags': user.team.correct_flags, 'wrong_flags': user.team.wrong_flags, 'solved': [], 'created': format(user.team.created, 'U')}).run(connection)
    except RqlRuntimeError as e:
        raise Exception('Error adding user team to realtime database: %s' % (e))
    finally:
        connection.close()

def insertCtfs(start, end):
    # Save the challenge flag to the database
    ctf = Ctf(start=start, end=end)
    ctf.save()

    # Push the realtime data to rethinkdb
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db(CTF_DB).table('ctfs').insert({ 'sid': ctf.id, 'start': format(ctf.start, 'U'), 'end': format(ctf.end, 'U'), 'created': format(ctf.created, 'U')}).run(connection)
    except RqlRuntimeError as e:
        raise Exception('Error adding ctf to realtime database: %s' % (e))
    finally:
        connection.close()


def insertCategories():
    # Save the category
    web = Category(name="Web")
    web.save()
    rookie = Category(name="Rookie")
    rookie.save()
    programming = Category(name="Programming")
    programming.save()
    crypto = Category(name="Crypto & Puzzles")
    crypto.save()
    advanced = Category(name="Advanced")
    advanced.save()
    data = Category(name="Data")
    data.save()
    bonus = Category(name="_Bonus")
    bonus.save()

    # Push test categories to rethinkdb database
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db(CTF_DB).table('categories').insert({'sid': web.id, 'name': web.name, 'created': format(web.created, 'U')}).run(connection)
        r.db(CTF_DB).table('categories').insert({'sid': rookie.id, 'name': rookie.name, 'created': format(rookie.created, 'U')}).run(connection)
        r.db(CTF_DB).table('categories').insert({'sid': programming.id, 'name': programming.name, 'created': format(programming.created, 'U')}).run(connection)
        r.db(CTF_DB).table('categories').insert({'sid': crypto.id, 'name': crypto.name, 'created': format(crypto.created, 'U')}).run(connection)
        r.db(CTF_DB).table('categories').insert({'sid': advanced.id, 'name': advanced.name, 'created': format(advanced.created, 'U')}).run(connection)
        r.db(CTF_DB).table('categories').insert({'sid': data.id, 'name': data.name, 'created': format(data.created, 'U')}).run(connection)
        r.db(CTF_DB).table('categories').insert({'sid': bonus.id, 'name': bonus.name, 'created': format(bonus.created, 'U')}).run(connection)
    except RqlRuntimeError as e:
        raise Exception('Error adding categories to realtime database: %s' % (e))
    finally:
        connection.close()

def insertRealTeams():
    try:
        with open('teams.json') as f:
            data = json.load(f)
            for team in data:
                makeUser(team['username'], team['email'], team['password'], False)
    except RqlRuntimeError as e:
        raise Exception('Error adding teams to realtime database: %s' % (e))


def insertRealChallenges():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        with open('challenges.json') as f:
            data = json.load(f)
            for c in data:
                category = Category.objects.filter(name__icontains = c['category'])
                if c['hosted']:
                    challenge = Challenge(category=category[0], flag=c['flag'], points=c['points'], title=c['title'], description=c['description'], hosted=c['hosted'], imageName=c['imageName'], ports=c['ports'], pathPrefix=c['pathPrefix'])
                else:
                    challenge = Challenge(category=category[0], flag=c['flag'], points=c['points'], title=c['title'], description=c['description'], hosted=c['hosted'])
                challenge.save()
                
                if c['hosted']:
                    r.db(CTF_DB).table('challenges').insert({ 'sid': challenge.id, 'category': challenge.category.id, 'title': c['title'], 'points': challenge.points, 'description': c['description'], 'solved_count': 0, 'hosted': c['hosted'], 'imageName': c['imageName'], 'ports': c['ports'], 'pathPrefix': c['pathPrefix'], 'created': format(challenge.created, 'U')}).run(connection)
                else:
                    r.db(CTF_DB).table('challenges').insert({ 'sid': challenge.id, 'category': challenge.category.id, 'title': c['title'], 'points': challenge.points, 'description': c['description'], 'solved_count': 0, 'hosted': c['hosted'], 'created': format(challenge.created, 'U')}).run(connection)

    except RqlRuntimeError as e:
        raise Exception('Error adding challenges to realtime database: %s' % (e))
    finally:
        connection.close()


def insertChallengeBoard():
    i = 1
    # Push test challenges to rethinkdb database
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        for category in Category.objects.all():
            # Save the challenge flag to the database
            challenge_50 = Challenge(category=category, flag="flag{0}".format(i), points=50, title='Test Title', description='Test Description', hosted=True, imageName='tutum/hello-world:latest', ports='80', pathPrefix="path{0}".format(i))
            challenge_50.save()
            i+=1

            # Save the challenge flag to the database
            challenge_100 = Challenge(category=category, flag="flag{0}".format(i), points=100, title='Test Title', description='Test Description', hosted=True, imageName='tutum/hello-world:latest', ports='80', pathPrefix="path{0}".format(i))
            challenge_100.save()
            i+=1

            # Save the challenge flag to the database
            challenge_200 = Challenge(category=category, flag="flag{0}".format(i), points=200, title='Test Title', description='Test Description', hosted=True, imageName='tutum/hello-world:latest', ports='80', pathPrefix="path{0}".format(i))
            challenge_200.save()
            i+=1

            # Save the challenge flag to the database
            challenge_300 = Challenge(category=category, flag="flag{0}".format(i), points=300, title='Test Title', description='Test Description', hosted=True, imageName='tutum/hello-world:latest', ports='80', pathPrefix="path{0}".format(i))
            challenge_300.save()
            i+=1

            # Save the challenge flag to the database
            challenge_400 = Challenge(category=category, flag="flag{0}".format(i), points=400, title='Test Title', description='Test Description', hosted=False)
            challenge_400.save()
            i+=1

            # Save the challenge flag to the database
            challenge_500 = Challenge(category=category, flag="flag{0}".format(i), points=500, title='Test Title', description='Test Description', hosted=False)
            challenge_500.save()
            i+=1

            r.db(CTF_DB).table('challenges').insert({ 'sid': challenge_50.id, 'category': challenge_50.category.id, 'title': 'Test Title', 'points': challenge_50.points, 'description': 'Test Description', 'solved_count': 0, 'hosted': True, 'imageName': 'tutum/hello-world:latest', 'ports': '80', 'pathPrefix': challenge_50.pathPrefix,'created': format(challenge_50.created, 'U')}).run(connection)
            r.db(CTF_DB).table('challenges').insert({ 'sid': challenge_100.id, 'category': challenge_100.category.id, 'title': 'Test Title', 'points': challenge_100.points, 'description': 'Test Description', 'solved_count': 0, 'hosted': True, 'imageName': 'tutum/hello-world:latest', 'ports': '80', 'pathPrefix': challenge_100.pathPrefix,'created': format(challenge_100.created, 'U')}).run(connection)
            r.db(CTF_DB).table('challenges').insert({ 'sid': challenge_200.id, 'category': challenge_200.category.id, 'title': 'Test Title', 'points': challenge_200.points, 'description': 'Test Description', 'solved_count': 0, 'hosted': True, 'imageName': 'tutum/hello-world:latest', 'ports': '80', 'pathPrefix': challenge_200.pathPrefix,'created': format(challenge_200.created, 'U')}).run(connection)
            r.db(CTF_DB).table('challenges').insert({ 'sid': challenge_300.id, 'category': challenge_300.category.id, 'title': 'Test Title', 'points': challenge_300.points, 'description': 'Test Description', 'solved_count': 0, 'hosted': True, 'imageName': 'tutum/hello-world:latest', 'ports': '80', 'pathPrefix': challenge_300.pathPrefix,'created': format(challenge_300.created, 'U')}).run(connection)
            r.db(CTF_DB).table('challenges').insert({ 'sid': challenge_400.id, 'category': challenge_400.category.id, 'title': 'Test Title', 'points': challenge_400.points, 'description': 'Test Description', 'solved_count': 0, 'hosted': False, 'created': format(challenge_400.created, 'U')}).run(connection)
            r.db(CTF_DB).table('challenges').insert({ 'sid': challenge_500.id, 'category': challenge_500.category.id, 'title': 'Test Title', 'points': challenge_500.points, 'description': 'Test Description', 'solved_count': 0, 'hosted': False, 'created': format(challenge_500.created, 'U')}).run(connection)


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
    parser.add_argument('--rteams', action="store_true", dest="rteams", help='Insert Real Users')
    parser.add_argument('--rchals', action="store_true", dest="rchals", help='Insert Real Challenges')

    args = parser.parse_args()

    resetRethinkDB()
    resetDjangoDB()
    makeAdminUser(args.admin_name, args.admin_email, args.admin_password, True)
    insertCtfs(start=timezone.now(), end=timezone.now() + timedelta(days=30))

    if args.cats:
        insertCategories()

    if args.chals:
        insertChallengeBoard()

    if args.rteams:
        # you must have a teams.json file in same directory
        insertRealTeams()
        makeUser('theWatchers', 'watchers@gmail.com', 'WatchersOnTheWall', True)
    else:
        makeUser('team2', 'team2@gmail.com', 'Password123!', False)
        makeUser('team3', 'team3@gmail.com', 'Password123!', False)
        makeUser('team4', 'team4@gmail.com', 'Password123!', False)
        makeUser('team5', 'team5@gmail.com', 'Password123!', False)
        makeUser('team6', 'team6@gmail.com', 'Password123!', False)
        makeUser('team7', 'team7@gmail.com', 'Password123!', False)
        makeUser('team8', 'team8@gmail.com', 'Password123!', False)
        makeUser('team9', 'team9@gmail.com', 'Password123!', False)
        makeUser('team10', 'team10@gmail.com', 'Password123!', False)

    if args.rchals:
        # you must have a challenge.json file in same directory
        insertRealChallenges()

    
    
