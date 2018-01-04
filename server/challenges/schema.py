import graphene
from graphene_django import DjangoObjectType
from users.validators import validate_user_is_admin, validate_user_is_authenticated
from challenges.validators import validate_flag, validate_flag_unique, validate_points
from challenges.models import Challenge

class AddChallenge(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        category = graphene.String(required=True)
        title = graphene.String(required=True)
        points = graphene.Int(required=True)
        description = graphene.String(required=True)
        flag = graphene.String(required=True)

    def mutate(self, info, category, title, points, description, flag):
        # Validate user is admin
        validate_user_is_admin(info.context.user)

        # Sanitize inputs 
        validate_flag(flag)
        validate_flag_unique(flag)
        validate_points(points)

        # Save the challenge flag to the database
        challenge = Challenge(flag=flag, points=points)
        challenge.save()

        # Push the realtime data to rethinkdb
        # save_to_rethinkdb(challenge.id, category, title, points, description)

        return AddChallenge(status='Challenge Created')


class CheckFlag(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        flag = graphene.String(required=True)

    def mutate(self, info, flag):
        user = info.context.user
        # Validate user is authenticated
        validate_user_is_authenticated(user)

        # Sanitize flag input 
        validate_flag(flag)

        if Challenge.objects.filter(flag__iexact=flag).exists():
            user.team.points += Challenge.objects.get(flag__iexact=flag).points
            return CheckFlag(status='Correct Flag') 
        else:
            return CheckFlag(status='Wrong Flag') 


class Mutation(graphene.ObjectType):
    add_challenge = AddChallenge.Field()
    check_flag = CheckFlag.Field()