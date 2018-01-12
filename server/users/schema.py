import graphene
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from redctf.settings import RDB_HOST, RDB_PORT, CTF_DB
from graphene_django import DjangoObjectType
from users.models import User
from teams.models import Team
from users.validators import validate_username, validate_password, validate_email, validate_username_unique, validate_email_unique, validate_user_is_authenticated
from django.contrib.auth import authenticate, login, logout

# ======================== #
# Temp fix for stage 1 dev #
# ======================== # 
import uuid
from teams.models import Team
# ======================== #
# Temp fix for stage 1 dev #
# ======================== #


class Me(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ('id', 'username', 'is_superuser')
        filter_fields = ('id', 'username', 'is_superuser')


class CreateUser(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        # Validate username, password, and email
        validate_username(username) 
        validate_username_unique(username) 
        validate_email(email)
        validate_email_unique(email)
        validate_password(password)

        # ======================== #
        # Temp fix for stage 1 dev #
        # ======================== # 
        token = str(uuid.uuid4())
        while Team.objects.filter(token__iexact=token).exists():
            token = str(uuid.uuid4())

        team = Team(name=username, token=token)
        team.save()
        # ======================== #
        # Temp fix for stage 1 dev #
        # ======================== # 

        user = User(
            username=username,
            email=email,
            team=team,
        )
        user.set_password(password)
        user.save()

        # ======================== #
        # Temp fix for stage 1 dev #
        # ======================== # 
        # Push the realtime data to rethinkdb
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        try:
            r.db(CTF_DB).table('teams').insert({ 'sid': team.id, 'points': team.points, 'correct_flags': team.correct_flags, 'wrong_flags': team.wrong_flags, 'solved': list(team.solved.all().values_list('id', flat=True))}).run(connection)
        except RqlRuntimeError as e:
            raise Exception('Error adding category to realtime database: %s' % (e))
        finally:
            connection.close()
        # ======================== #
        # Temp fix for stage 1 dev #
        # ======================== # 

        return CreateUser(status='User account created')


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
    login = LogIn.Field()
    logout = LogOut.Field()
