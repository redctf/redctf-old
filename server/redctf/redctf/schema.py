import graphene
import challenges.schema
import users.schema

class Query(users.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, challenges.schema.Mutation, graphene.ObjectType,):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)