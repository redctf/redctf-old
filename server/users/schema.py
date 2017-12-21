import graphene
from graphene_django import DjangoObjectType
from users.models import User
from users.validators import validate_username, validate_password, validate_email
from django.contrib.auth import authenticate, login, logout


class UserType(DjangoObjectType):
    class Meta:
        model = User


class CreateUser(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        # Validate username, password, and email
        validate_username(username)
        validate_password(password)
        validate_email(email)

        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(status='User account created')


class LogIn(graphene.Mutation):
    id = graphene.Int()
    isAdmin = graphene.Int()

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    def mutate(self, info, username, password):
        # Validate username and password
        validate_username(username)
        validate_password(password)

        user = authenticate(username=username, password=password)

        if not user:
            raise Exception('Invalid username or password')

        login(info.context, user)

        return LogIn(id=user.id, isAdmin=user.is_superuser)
    
class LogOut(graphene.Mutation):
    status = graphene.String()

    def mutate(self, info):
        logout(info.context) 
        return LogOut(status='Logged Out')

class Query(object):
    me = graphene.String()

    def resolve_me(self, info):
        user = info.context.user
        if info.context.user.is_anonymous:
            raise Exception('Not authenticated')

        return info.context.user.username


class Mutation(object):
    create_user = CreateUser.Field()
    login = LogIn.Field()
    logout = LogOut.Field()
