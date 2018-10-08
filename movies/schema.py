import graphene
from django.shortcuts import get_object_or_404
from graphene_django.filter import DjangoFilterConnectionField

from graphene_django.types import DjangoObjectType
from graphql_relay import from_global_id

from movies.models import Movie, Comment


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'genre': ['exact', 'icontains'],
            'year': ['exact', 'gt', 'lt'],
        }
        interfaces = (graphene.relay.Node,)


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        interfaces = (graphene.relay.Node,)


class CreateMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        year = graphene.Int(required=False)

    movie = graphene.Field(lambda: MovieType)

    def mutate(self, info, title, year=None):
        new_movie = Movie.objects.create(title=title, year=year)
        return CreateMovie(movie=new_movie)


class MovieMutation(graphene.ObjectType):
    create_movie = CreateMovie.Field()


class MovieQuery(object):
    movie = graphene.Field(
        MovieType,
        id=graphene.String(),
        title=graphene.String()
    )
    all_movies = DjangoFilterConnectionField(MovieType)

    def resolve_movie(self, info, **kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')

        if id is not None:
            return Movie.objects.get(pk=from_global_id(id)[-1])

        if title is not None:
            return Movie.objects.get(title=title)

        return None


class CommentQuery(object):
    comment = graphene.Field(
        CommentType,
        id=graphene.String(),
    )

    all_comments = graphene.List(CommentType)

    def resolve_all_comments(self, info, **kwargs):
        return Comment.objects.all()

    def resolve_comment(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Comment.objects.get(pk=from_global_id(id)[-1])

        return None


class CreateComment(graphene.Mutation):
    id = graphene.String()
    body = graphene.String()
    movie = graphene.Field(MovieType)

    class Arguments:
        body = graphene.String()
        movie_id = graphene.String()

    def mutate(self, info, body, movie_id):
        movie_row_id = from_global_id(movie_id)[-1]
        movie = get_object_or_404(Movie, id=movie_row_id)
        comment = Comment(body=body, movie=movie)
        comment.save()

        return CreateComment(
            id=comment.id,
            body=comment.body,
            movie=movie
        )


class CommentMutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
