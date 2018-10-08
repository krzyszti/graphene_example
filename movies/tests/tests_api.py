import snapshottest

from django import test

from graphene.test import Client

from graph_test.schema import schema
from movies.models import Movie


class AllMoviesAPITestCase(test.TestCase, snapshottest.TestCase):
    """
    Testing the API for allMovies

    Django TestCase is required for database cleanup between tests.
    """

    def setUp(self):
        self.client = Client(schema)

    def test_no_movies(self):
        """
        no movies created, should return empty list
        """
        query = "query { allMovies { edges { node { id title } } } }"

        self.assertMatchSnapshot(self.client.execute(query))

    def test_one_movie(self):
        """
        one movie created, should return one element list
        """
        Movie(title='Test').save()

        query = "query { allMovies { edges { node { id title } } } }"

        self.assertMatchSnapshot(self.client.execute(query))

    def test_multiple_movies(self):
        """
        one movie created, should return one element list
        """
        Movie(title='Test1').save()
        Movie(title='Test2').save()

        query = "query { allMovies { edges { node { id title } } } }"

        self.assertMatchSnapshot(self.client.execute(query))

    def test_movie_year_filter(self):
        """
        two movies created with different years, should return only one of them
        """
        Movie(title='Test1', year=1990).save()
        Movie(title='Test2', year=2005).save()

        query = "query { allMovies(year_Lt: 2000) { edges { node { id title year } } } }"

        self.assertMatchSnapshot(self.client.execute(query))


class MovieMutationAPITestCase(test.TestCase, snapshottest.TestCase):
    def setUp(self):
        self.client = Client(schema)
        self.movies_initial_count = Movie.objects.all().count()

    def test_movie_create_all_required_fields_present(self):
        """
        one movie created, should return one element list
        """

        mutation = 'mutation { createMovie(title: "Test") { movie { id title year } } }'

        self.assertMatchSnapshot(self.client.execute(mutation))

        self.assertEqual(Movie.objects.all().count(), self.movies_initial_count + 1)

    def test_movie_create_title_missing(self):
        """
        one movie created, should return one element list
        """

        mutation = 'mutation { createMovie { movie { id title year } } }'

        self.assertMatchSnapshot(self.client.execute(mutation))

        self.assertEqual(Movie.objects.all().count(), self.movies_initial_count)

    def test_movie_create_additional_fields_present(self):
        """
        one movie created, should return one element list
        """

        mutation = 'mutation { createMovie(title: "Test", year: 2005) { movie { id title year } } }'

        self.assertMatchSnapshot(self.client.execute(mutation))

        self.assertEqual(Movie.objects.all().count(), self.movies_initial_count + 1)
