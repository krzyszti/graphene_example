import graphene

import movies.schema


class Query(
            movies.schema.MovieQuery,
            movies.schema.CommentQuery,
            graphene.ObjectType
           ):
    """
    This class will inherit from multiple Queries
    as we begin to add more apps to our project
    """
    pass


class Mutation(
                movies.schema.MovieMutation,
                movies.schema.CommentMutation,
                graphene.ObjectType
              ):
    """
    This class will inherit from multiple Mutations
    as we begin to add more apps to our project
    """
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
