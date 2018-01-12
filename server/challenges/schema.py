import graphene
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from redctf.settings import RDB_HOST, RDB_PORT, CTF_DB
from graphene_django import DjangoObjectType
from users.validators import validate_user_is_admin, validate_user_is_authenticated
from challenges.validators import validate_flag, validate_flag_unique, validate_points
from categories.models import Category
from challenges.models import Challenge

class AddChallenge(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        category = graphene.Int(required=True)
        title = graphene.String(required=True)
        points = graphene.Int(required=True)
        description = graphene.String(required=True)
        flag = graphene.String(required=True)

    def mutate(self, info, category, title, points, description, flag):
        # Validate user is admin
        validate_user_is_admin(info.context.user)

        # TODO: sanitize all the input fields 
        validate_flag(flag)
        validate_flag_unique(flag)
        validate_points(points)

        challenge_category = Category.objects.get(id=category)

        # Save the challenge flag to the database
        challenge = Challenge(category=challenge_category, flag=flag, points=points)
        challenge.save()

        # Push the realtime data to rethinkdb
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        try:
            r.db(CTF_DB).table('challenges').insert({ 'sid': challenge.id, 'category': category, 'title': title, 'points': points, 'description': description }).run(connection)
        except RqlRuntimeError as e:
            raise Exception('Error adding challenge to realtime database: %s' % (e))
        finally:
            connection.close()

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

        correct = False
        if Challenge.objects.filter(flag__iexact=flag).exists():
            chal = Challenge.objects.get(flag__iexact=flag)
            if chal not in user.team.solved.all():
                user.team.points += chal.points
                user.team.correct_flags += 1
                user.team.solved.add(chal)
                user.team.save()
            correct = True
        else:
            user.team.wrong_flags += 1    
            user.team.save()
            correct = False
             
        # Push the realtime data to rethinkdb
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        try:
            r.db(CTF_DB).table('teams').filter({"sid": user.team.id}).update({'points': user.team.points, 'correct_flags': user.team.correct_flags, 'wrong_flags': user.team.wrong_flags, 'solved': list(user.team.solved.all().values_list('id', flat=True))}).run(connection)
        except RqlRuntimeError as e:
            raise Exception('Error adding category to realtime database: %s' % (e))
        finally:
            connection.close()
        
        if correct:
            return CheckFlag(status='Correct Flag') 
        else:
            return CheckFlag(status='Wrong Flag')


class Mutation(graphene.ObjectType):
    add_challenge = AddChallenge.Field()
    check_flag = CheckFlag.Field()