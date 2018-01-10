import graphene
from graphene_django import DjangoObjectType
from users.validators import validate_user_is_admin, validate_user_is_authenticated
from categories.validators import validate_name, validate_name_unique
from categories.models import Category

class AddCategory(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        name = graphene.String(required=True)


    def mutate(self, info, name):
        # Validate user is admin
        validate_user_is_admin(info.context.user)

        # Sanitize inputs 
        validate_name(name)
        validate_name_unique(name)

        # Save the category
        category = Category(name=name)
        category.save()


        return AddCategory(status='Category Created')



class Mutation(graphene.ObjectType):
    add_category = AddCategory.Field()