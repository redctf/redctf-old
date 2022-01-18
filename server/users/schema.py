import graphene
import rethinkdb as r
import threading
from dockerAPI.dockerAPI import *
# from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from redctf.settings import CTF_DB
from graphene_django import DjangoObjectType
from django.utils.dateformat import format
from django.utils import timezone
from users.models import User
from teams.models import Team
from ctfs.models import Ctf
from containers.models import Container
from users.validators import validate_username, validate_password, validate_email, validate_username_unique, validate_email_unique, validate_user_is_authenticated, validate_user_is_admin
from teams.validators import validate_token
from django.contrib.auth import authenticate, login, logout
from containers.schema import *
from django.contrib.auth.signals import user_logged_in, user_logged_out


d = dockerAPI()


# # ======================== #
# # Temp fix for stage 1 dev #
# # ======================== #
# import uuid
# from teams.models import Team
# # ======================== #
# # Temp fix for stage 1 dev #
# # ======================== #

def perform_some_action_on_login(sender, user, **kwargs):
    """
    A signal receiver which performs some actions for
    the user logging in.
    """

    # your code here
    print("caught logged in signal")

    try:
        threadedScaleAllChallenges()

    except Exception as ex:
        raise Exception(
            'unknown issue with login')

    return


def perform_some_action_on_logout(sender, user, **kwargs):
    """
    A signal receiver which performs some actions for
    the user logging out.
    """

    # your code here
    print("caught logged out signal")
    # destroy all user's containers
    try:
        # scaleAllChallenges()
        
        processContainersOnLogout(user)

    except Exception as ex:
        raise Exception(
            'unknown issue with logout')

    return

def processContainersOnLogout(user):
    
    # look up container that belongs to logged in user
    try:
        cont_objs = Container.objects.filter(user__exact=user)

        if len(cont_objs) == 0:
            print('No containers assigned to user.')

        for cont in cont_objs:
            removeContainer(cont)
            
        scaleAllChallenges()

    except:
        print('Container does not exist for user.')
        # if none exists, log out
        
user_logged_in.connect(perform_some_action_on_login)
user_logged_out.connect(perform_some_action_on_logout)


class Me(DjangoObjectType):
    class Meta:
        model = User
        # only_fields = ('id', 'username', 'is_superuser')
        # filter_fields = ('id', 'username', 'is_superuser')


class TeamType(DjangoObjectType):
    class Meta:
        model = Team


class CreateUser(graphene.Mutation):
    status = graphene.String()
    user = graphene.Field(Me)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        hidden = graphene.Boolean(required=True)
        token = graphene.String(required=True)

    def mutate(self, info, username, password, email, hidden, token):

        # Validate active Ctf
        if Ctf.objects.filter(start__lt=timezone.now(), end__gt=timezone.now()):

            # Validate username, password, and email
            validate_username(username)
            validate_username_unique(username)
            validate_email(email)
            validate_email_unique(email)
            # validate_password(password)

            # Validate token
            validate_token(token)

            if not Team.objects.filter(token__iexact=token).exists():
                raise Exception('Invalid team token')

            # # ======================== #
            # # Temp fix for stage 1 dev #
            # # ======================== #
            # token = str(uuid.uuid4())
            # while Team.objects.filter(token__iexact=token).exists():
            #     token = str(uuid.uuid4())

            # team = Team(name=username, token=token, hidden=hidden)
            # team.save()
            # # ======================== #
            # # Temp fix for stage 1 dev #
            # # ======================== #

            user = User(
                username=username,
                email=email,
                team=Team.objects.get(token=token),
                hidden=hidden
            )
            user.set_password(password)
            user.save()
            
            try: 
                threadedScaleAllChallenges()
            except Exception as ex:
                raise Exception('error when registering user')

            # # ======================== #
            # # Temp fix for stage 1 dev #
            # # ======================== #
            # # Push the realtime data to rethinkdb
            # connection = r.connect(host=RDB_HOST, port=RDB_PORT)
            # try:
            #     r.db(CTF_DB).table('teams').insert({ 'sid': user.team.id, 'name': user.team.name, 'points': user.team.points, 'hidden': user.team.hidden, 'correct_flags': user.team.correct_flags, 'wrong_flags': user.team.wrong_flags, 'solved': [], 'created': format(user.team.created, 'U')}).run(connection)
            # except RqlRuntimeError as e:
            #     raise Exception('Error adding team to realtime database: %s' % (e))
            # finally:
            #     connection.close()
            # # ======================== #
            # # Temp fix for stage 1 dev #
            # # ======================== #

            return CreateUser(status='User account created', user=user)

        else:
            #no active ctf
            raise Exception('No currently active CTF')


class ChangePassword(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        password = graphene.String(required=True)

    def mutate(self, info, password):
        user = info.context.user
        # Validate user is authenticated
        validate_user_is_authenticated(user)
        # validate_password(password)

        user.set_password(password)
        user.save()

        return ChangePassword(status='User password changed')


class LogIn(graphene.Mutation):
    id = graphene.Int()
    token = graphene.String()
    username = graphene.String()
    isSuperuser = graphene.Int()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        # Validate username and password
        validate_username(username)
        # validate_password(password)

        user = authenticate(username=username, password=password)

        if not user:
            raise Exception('Invalid username or password')

        login(info.context, user)

        token=str("test")
        username=str("test_username")
        return LogIn(id=user.id, token=token, username=username, isSuperuser=user.is_superuser)


class LogOut(graphene.Mutation):
    status = graphene.String()

    def mutate(self, info):
        user = info.context.user

        logout(info.context)
        return LogOut(status='Logged Out')


class Query(object):
    me = graphene.Field(Me)

    def resolve_me(self, info):
        user = info.context.user
        validate_user_is_authenticated(user)

        return user


class UpdateUser(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=False)
        email = graphene.String(required=False)
        hidden = graphene.Boolean(required=False)
        token = graphene.String(required=False)
        active = graphene.Boolean(required=False)
        newUsername = graphene.String(required=False)

    def mutate(self, info, username, password=None, email=None, hidden=None, token=None, active=None, newUsername=None):

        user = info.context.user
        # Validate user is admin
        validate_user_is_admin(user)

        if User.objects.filter(username__iexact=username).exists():
            targetUser = User.objects.get(username__iexact=username)

            if newUsername is not None:
                validate_username(newUsername)
                validate_username_unique(newUsername)
                targetUser.username = newUsername

            if password is not None:
                targetUser.set_password = password

            if email is not None:
                validate_email(email)
                validate_email_unique(email)
                targetUser.email = email

            if hidden is not None:
                targetUser.hidden = hidden

            if active is not None:
                targetUser.active = active

            targetUser.save()

        else:
            raise Exception('Error - can\'t find user: %s' % (username))

        return UpdateUser(status='User Updated: %s' % (username))


class DeleteUser(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        username = graphene.String(required=True)

    def mutate(self, info, username):
        user = info.context.user
        # Validate user is admin
        validate_user_is_admin(user)

        if User.objects.filter(username__iexact=username).exists():
            targetUser = User.objects.get(username__iexact=username)

            try:
                targetUser.delete()

            except Exception as ex:
                raise Exception('error with user delete: {0}'.format(ex))

        else:
            print('no matching usernames')

        return DeleteUser(status='Username Deleted: %s' % (username))


class Mutation(object):
    create_user = CreateUser.Field()
    change_password = ChangePassword.Field()
    login = LogIn.Field()
    logout = LogOut.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
