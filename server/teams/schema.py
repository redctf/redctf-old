import graphene
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from redctf.settings import RDB_HOST, RDB_PORT, CTF_DB
import uuid
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from users.schema import CreateUser
from users.models import User
from teams.models import Team
from users.validators import validate_user_is_admin, validate_user_is_authenticated
from teams.validators import validate_teamname, validate_token, validate_teamname_unique 

class TeamType(DjangoObjectType):
    class Meta:
        model = Team

class CreateTeam(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        teamname = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        hidden = graphene.String(required=True)
        token = graphene.String(required=False)

    def mutate(self, info, teamname, username, email, password, hidden):
        # Validate teamname
        validate_teamname(teamname) 
        validate_teamname_unique(teamname)

        # Create unique team token
        token = str(uuid.uuid4())
        while Team.objects.filter(token__iexact=token).exists():
            token = str(uuid.uuid4())

        # Create and Save Team
        team = Team(name=teamname, token=token, hidden=hidden)
        team.save()

        # Create User and Assign to Team
        # Make mutation
        mutation = 'createUser( username:' + username +', email:' + email + ', password:' + password + ', hidden:' + hidden + ', token' + token + ')'
        user = CreateUser(mutation)

        # Return Success
        return CreateTeam(status='Created Team and User Successfully')


class JoinTeam(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        hidden = graphene.String(required=True)

    def mutate(self, info, token):
        # Validate username and password
        user = info.context.user
        validate_user_is_authenticated(user)
        validate_token(token)

        if not Team.objects.filter(token__iexact=token).exists():
            raise Exception('Invalid team token')
        
        team = Team.objects.get(token=token)
        user.team = team
        user.save()

        return JoinTeam(status='Join team successful')
    

class Query(object):
    team = graphene.Field(TeamType) 

    def resolve_team(self, info):
        user = info.context.user
        validate_user_is_authenticated(user)

        if not user.team:
            raise Exception('User has not joined a team')

        return user.team


class Mutation(object):
    create_team = CreateTeam.Field()
    join_team = JoinTeam.Field()