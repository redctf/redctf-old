import graphene
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from redctf.settings import RDB_HOST, RDB_PORT, CTF_DB
from graphene_django import DjangoObjectType
from django.utils.dateformat import format
from users.models import User
from teams.models import Team
from users.validators import validate_username, validate_password, validate_email, validate_username_unique, validate_email_unique, validate_user_is_authenticated
from teams.validators import validate_token
from django.contrib.auth import authenticate, login, logout

# # ======================== #
# # Temp fix for stage 1 dev #
# # ======================== #
# import uuid
# from teams.models import Team
# # ======================== #
# # Temp fix for stage 1 dev #
# # ======================== #


class Me(DjangoObjectType):
    class Meta:
        model = User
        #only_fields = ('id', 'username', 'is_superuser')
        #filter_fields = ('id', 'username', 'is_superuser')

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
        # Validate username, password, and email
        validate_username(username)
        validate_username_unique(username)
        validate_email(email)
        validate_email_unique(email)
        validate_password(password)

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
            team = Team.objects.get(token=token),
            hidden=hidden
        )
        user.set_password(password)
        user.save()

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

class ChangePassword(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        password = graphene.String(required=True)

    def mutate(self, info, password):
        user = info.context.user
        # Validate user is authenticated
        validate_user_is_authenticated(user)
        validate_password(password)

        user.set_password(password)
        user.save()

        return ChangePassword(status='User password changed')


class LogIn(graphene.Mutation):
    id = graphene.Int()
    isSuperuser = graphene.Int()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        # Validate username and password
        validate_username(username)
        validate_password(password)

        user = authenticate(username=username, password=password)

        print (user)
        if not user:
            raise Exception('Invalid username or password')

        login(info.context, user)

        return LogIn(id=user.id, isSuperuser=user.is_superuser)

class LogOut(graphene.Mutation):
    status = graphene.String()

    def mutate(self, info):
        logout(info.context)
        return LogOut(status='Logged Out')

class Query(object):
    me = graphene.Field(Me)

    def resolve_me(self, info):
        user = info.context.user
        validate_user_is_authenticated(user)

        return user


class Mutation(object):
    create_user = CreateUser.Field()
    change_password = ChangePassword.Field()
    login = LogIn.Field()
    logout = LogOut.Field()
