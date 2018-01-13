import graphene
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from redctf.settings import RDB_HOST, RDB_PORT, CTF_DB
from graphene_django import DjangoObjectType
from users.validators import validate_user_is_admin
from categories.validators import validate_name, validate_name_unique
from categories.models import Category

class AddCategory(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        name = graphene.String(required=True)


    def mutate(self, info, name):
        user = info.context.user
        # Validate user is admin
        validate_user_is_admin(user)

        # Sanitize inputs 
        validate_name(name)
        validate_name_unique(name)

        # Save the category
        category = Category(name=name)
        category.save()

        # Push the realtime data to rethinkdb
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        try:
            r.db(CTF_DB).table('categories').insert({ 'sid': category.id, 'name': name }).run(connection)
        except RqlRuntimeError as e:
            raise Exception('Error adding category to realtime database: %s' % (e))
        finally:
            connection.close()


        return AddCategory(status='Category Created')



class Mutation(graphene.ObjectType):
    add_category = AddCategory.Field()