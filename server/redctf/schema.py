import graphene
import challenges.schema
import users.schema
import teams.schema
import categories.schema

class Query(users.schema.Query, teams.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, teams.schema.Mutation, challenges.schema.Mutation, categories.schema.Mutation, graphene.ObjectType,):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)