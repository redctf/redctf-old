import graphene
import uuid
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from users.schema import *
from users.models import User
from teams.models import Team
from ctfs.models import Ctf
from users.validators import validate_username, validate_password, validate_email, validate_username_unique, validate_email_unique, validate_user_is_admin, validate_user_is_authenticated
from teams.validators import validate_teamname, validate_token, validate_teamname_unique
from django.utils import timezone

class TeamType(DjangoObjectType):
    class Meta:
        model = Team

class CreateTeam(graphene.Mutation):
    status = graphene.String()
    token = graphene.String()
    team = graphene.Field(TeamType)

    class Arguments:
        teamname = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        hidden = graphene.Boolean(required=True)

    def mutate(self, info, teamname, username, email, password, hidden):
            
        # Validate active Ctf
        if Ctf.objects.filter(start__lt=timezone.now(), end__gt=timezone.now()):

            # Validate teamname
            validate_teamname(teamname)
            validate_teamname_unique(teamname)

            # Validate username, password, and email
            validate_username(username)
            validate_username_unique(username)
            validate_email(email)
            validate_email_unique(email)
            # validate_password(password)


            # Create unique team token
            token = str(uuid.uuid4())
            while Team.objects.filter(token__iexact=token).exists():
                token = str(uuid.uuid4())

            # Create and Save Team
            team = Team(name=teamname, token=token, hidden=hidden)
            team.save()

            # Return Success
            return CreateTeam(status=('Created Team Successfully'), token=token)

        else:
            #no active ctf
            raise Exception('No currently active CTF')


class JoinTeam(graphene.Mutation):
    ####NOT CURRENTLY USED####
    status = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        hidden = graphene.Boolean(required=True)

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
