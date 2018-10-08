# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['AllMoviesAPITestCase::test_movie_year_filter 1'] = {
    'data': {
        'allMovies': {
            'edges': [
                {
                    'node': {
                        'id': 'TW92aWVUeXBlOjE=',
                        'title': 'Test1',
                        'year': 1990
                    }
                }
            ]
        }
    }
}

snapshots['AllMoviesAPITestCase::test_multiple_movies 1'] = {
    'data': {
        'allMovies': {
            'edges': [
                {
                    'node': {
                        'id': 'TW92aWVUeXBlOjE=',
                        'title': 'Test1'
                    }
                },
                {
                    'node': {
                        'id': 'TW92aWVUeXBlOjI=',
                        'title': 'Test2'
                    }
                }
            ]
        }
    }
}

snapshots['AllMoviesAPITestCase::test_no_movies 1'] = {
    'data': {
        'allMovies': {
            'edges': [
            ]
        }
    }
}

snapshots['AllMoviesAPITestCase::test_one_movie 1'] = {
    'data': {
        'allMovies': {
            'edges': [
                {
                    'node': {
                        'id': 'TW92aWVUeXBlOjE=',
                        'title': 'Test'
                    }
                }
            ]
        }
    }
}

snapshots['MovieMutationAPITestCase::test_movie_create_additional_fields_present 1'] = {
    'data': {
        'createMovie': {
            'movie': {
                'id': 'TW92aWVUeXBlOjE=',
                'title': 'Test',
                'year': 2005
            }
        }
    }
}

snapshots['MovieMutationAPITestCase::test_movie_create_all_required_fields_present 1'] = {
    'data': {
        'createMovie': {
            'movie': {
                'id': 'TW92aWVUeXBlOjE=',
                'title': 'Test',
                'year': 0
            }
        }
    }
}

snapshots['MovieMutationAPITestCase::test_movie_create_title_missing 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 12,
                    'line': 1
                }
            ],
            'message': 'Field "createMovie" argument "title" of type "String!" is required but not provided.'
        }
    ]
}
