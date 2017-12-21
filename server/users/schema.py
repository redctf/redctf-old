import graphene
from graphene_django import DjangoObjectType
from users.models import User
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

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            raise Exception('Username or email not available')

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
