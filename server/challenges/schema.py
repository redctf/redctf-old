import graphene
from graphene_django import DjangoObjectType
from users.validators import validate_user_is_admin
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

        # Save the challenge flag to the database
        challenge = Challenge(flag=flag)
        challenge.save()

        # Push the realtime data to rethinkdb
        # save_to_rethinkdb(challenge.id, category, title, points, description)

        return AddChallenge(status='Challenge Created')


class Mutation(graphene.ObjectType):
    add_challenge = AddChallenge.Field()