# Hack to use django app models in standalone script
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "redctf.settings")
django.setup()

# Imports
import argparse, contextlib, uuid
import json
from django.utils.dateformat import format
from django.utils import timezone
from datetime import timedelta
from redctf.settings import DATABASES
from users.models import User
from teams.models import Team
from categories.models import Category
from challenges.models import Challenge
from ctfs.models import Ctf
from containers.models import Container
from users.validators import validate_username, validate_password, validate_email


def resetDjangoDB():
    # Remove database file if exists
    with contextlib.suppress(FileNotFoundError):
        os.remove(DATABASES['default']['NAME'])
    
    # Clear all data from django db
    os.system('python3 manage.py flush --no-input')
    
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


def insertCtfs(start, end):
    # Save the challenge flag to the database
    ctf = Ctf(start=start, end=end)
    ctf.save()


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


def insertRealTeams():
    try:
        with open('teams.json') as f:
            data = json.load(f)
            for team in data:
                makeUser(team['username'], team['email'], team['password'], False)
    except Exception as e:
         raise Exception('Error adding teams to realtime database: %s' % (e))


def insertRealChallenges():
    try:
        with open('challenges.json') as f:
            data = json.load(f)
            for c in data:
                category = Category.objects.filter(name__icontains = c['category'])
                if c['hosted']:
                    challenge = Challenge(category=category[0], flag=c['flag'], points=c['points'], title=c['title'], description=c['description'], hosted=c['hosted'], fileUpload=c['fileUpload'], imageName=c['imageName'], ports=c['ports'], pathPrefix=c['pathPrefix'])
                else:
                    challenge = Challenge(category=category[0], flag=c['flag'], points=c['points'], title=c['title'], description=c['description'], hosted=c['hosted'], fileUpload=c['fileUpload'])
                challenge.save()
                
    except Exception as e:
        raise Exception('Error adding challenges to database: %s' % (e))


def insertChallengeBoard():
    i = 1
    # Push test challenges to database
    try:
        for category in Category.objects.all():
            # Save the challenge flag to the database
            challenge_50 = Challenge(category=category, flag="flag{0}".format(i), points=50, title='Test Title', description='Test Description', hosted=True, fileUpload=False, imageName='tutum/hello-world:latest', ports='80', pathPrefix="path{0}".format(i))
            challenge_50.save()
            i+=1

            # Save the challenge flag to the database
            challenge_100 = Challenge(category=category, flag="flag{0}".format(i), points=100, title='Test Title', description='Test Description', hosted=True, fileUpload=False, imageName='tutum/hello-world:latest', ports='80', pathPrefix="path{0}".format(i))
            challenge_100.save()
            i+=1

            # Save the challenge flag to the database
            challenge_200 = Challenge(category=category, flag="flag{0}".format(i), points=200, title='Test Title', description='Test Description', hosted=True, fileUpload=False, imageName='tutum/hello-world:latest', ports='80', pathPrefix="path{0}".format(i))
            challenge_200.save()
            i+=1

            # Save the challenge flag to the database
            challenge_300 = Challenge(category=category, flag="flag{0}".format(i), points=300, title='Test Title', description='Test Description', hosted=False, fileUpload=True)
            challenge_300.save()
            i+=1

            # Save the challenge flag to the database
            challenge_400 = Challenge(category=category, flag="flag{0}".format(i), points=400, title='Test Title', description='Test Description', hosted=False, fileUpload=False)
            challenge_400.save()
            i+=1

            # Save the challenge flag to the database
            challenge_500 = Challenge(category=category, flag="flag{0}".format(i), points=500, title='Test Title', description='Test Description', hosted=False, fileUpload=False)
            challenge_500.save()
            i+=1

    except Exception as e:
        raise Exception('Error adding challenges to database: %s' % (e))
    

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

    
    
