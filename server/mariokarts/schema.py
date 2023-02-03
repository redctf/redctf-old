import graphene
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from redctf.settings import RDB_HOST, RDB_PORT, CTF_DB
from graphene_django import DjangoObjectType
from django.utils.dateformat import format
from django.utils import timezone
from users.validators import validate_user_is_admin
from mariokarts.validators import validate_name, validate_name_unique
from mariokarts.models import Mariokart
from ctfs.models import Ctf


class CheckBalloon(graphene.Mutation):
    shouldIPop = graphene.Boolean()
    balloonToPop = graphene.Int()

    class Arguments:
        guid = graphene.String(required=True)

    def mutate(self, info, guid):
        # user = info.context.user
        # # Validate user is authenticated
        # validate_user_is_authenticated(user)

        # Sanitize guid input
        #validate_guid(guid)

        # Validate active Ctf
        if Ctf.objects.filter(start__lt=timezone.now(), end__gt=timezone.now()):
            
            if guid == "test":
                correct=True
            else:
                correct=False


            if correct:
                return CheckBalloon(shouldIPop=True, balloonToPop=1)
            else:
                return CheckBalloon(shouldIPop=False)
        else:
            #no active ctf
            return CheckBalloon(status='No currently active CTF')

class Mutation(graphene.ObjectType):
    check_balloon = CheckBalloon.Field()