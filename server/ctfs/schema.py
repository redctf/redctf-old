import graphene
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from redctf.settings import RDB_HOST, RDB_PORT, CTF_DB
from graphene_django import DjangoObjectType
from django.utils.dateformat import format
from datetime import datetime, timezone
from users.validators import validate_user_is_admin, validate_user_is_authenticated
from ctfs.validators import validate_start, validate_end, validate_ctf_exists
from ctfs.models import Ctf

class CtfType(DjangoObjectType):
    class Meta:
        model = Ctf

class AddCtf(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        start = graphene.Int(required=True)
        end = graphene.Int(required=True)
        

    def mutate(self, info, start, end):
        user = info.context.user
        # Validate user is admin
        validate_user_is_admin(user)

        validate_start(start)
        validate_end(end)

        # Save the challenge flag to the database
        ctf = Ctf(start=datetime.fromtimestamp(int(start), timezone.utc), end=datetime.fromtimestamp(int(end), timezone.utc))
        ctf.save()

        # Push the realtime data to rethinkdb
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        try:
            r.db(CTF_DB).table('ctfs').insert({ 'sid': ctf.id, 'start': format(ctf.start, 'U'), 'end': format(ctf.end, 'U'), 'created': format(ctf.created, 'U')}).run(connection)
        except RqlRuntimeError as e:
            raise Exception('Error adding ctf to realtime database: %s' % (e))
        finally:
            connection.close()

        return AddCtf(status='Ctf Created')


class ModifyCtf(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        ctf_id = graphene.Int(required=True)
        start = graphene.Int(required=False)
        end = graphene.Int(required=False)
        

    def mutate(self, info, ctf_id, start, end):
        user = info.context.user
        # Validate user is admin
        validate_user_is_admin(user)

        if start and end:
            validate_start(start) 
            validate_end(end)
            ctf = Ctf.objects.get(id=ctf_id)
            ctf.start = datetime.fromtimestamp(int(start), timezone.utc)
            ctf.end = datetime.fromtimestamp(int(end), timezone.utc)
            ctf.save()
        elif start and not end:
            validate_start(start) 
            ctf = Ctf.objects.get(id=ctf_id)
            ctf.start = datetime.fromtimestamp(int(start), timezone.utc)
            ctf.save()
        elif not start and end:
            validate_start(start) 
            validate_end(end)
            ctf = Ctf.objects.get(id=ctf_id)
            ctf.end = datetime.fromtimestamp(int(end), timezone.utc)
            ctf.save()
        else:
            raise Exception('Must provide start or end time')

        # Push the realtime data to rethinkdb
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        try:
            r.db(CTF_DB).table('ctfs').insert({ 'sid': ctf.id, 'start': format(ctf.start, 'U'), 'end': format(ctf.end, 'U')}).run(connection)
        except RqlRuntimeError as e:
            raise Exception('Error adding ctf to realtime database: %s' % (e))
        finally:
            connection.close()

        return ModifyCtf(status='Ctf Modified')


class Mutation(graphene.ObjectType):
    add_ctf = AddCtf.Field()
    modify_ctf = ModifyCtf.Field()