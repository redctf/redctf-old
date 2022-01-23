import graphene
from graphene_django import DjangoObjectType
from django.utils.dateformat import format
from users.validators import validate_user_is_admin
from categories.validators import validate_name, validate_name_unique
from categories.models import Category

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


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

        return AddCategory(status='Category Created')


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    category_by_id = graphene.Field(CategoryType, id=graphene.String())

    def resolve_categories(root, info, **kwargs):
        # Querying a list
        return Category.objects.all()

    def resolve_category_by_id(root, info, id):
        # Querying a single object
        return Category.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    add_category = AddCategory.Field()