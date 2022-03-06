import graphene
import challenges.schema
import users.schema
import teams.schema
import categories.schema
import ctfs.schema
import containers.schema

class Query(users.schema.Query, teams.schema.Query, challenges.schema.Query, categories.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, teams.schema.Mutation, challenges.schema.Mutation, categories.schema.Mutation, ctfs.schema.Mutation, containers.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)