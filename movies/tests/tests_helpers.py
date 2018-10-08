from unittest import mock

import responses
from django.test import TestCase

from movies.helpers import get_movie_data_from_ombd


class TestGetMovieDataFromOmbd(TestCase):
    @staticmethod
    def _mock_response(content=b''):
        mock_resp = mock.Mock()
        mock_resp.content = content
        return mock_resp

    @mock.patch('movies.helpers.OMDB_API_TOKEN', '123')
    @mock.patch('movies.helpers.logger')
    @mock.patch('requests.get')
    def test_connection_error(self, request_get_mocked, logger_mocked):
        request_get_mocked.side_effect = [ConnectionError]

        self.assertEqual(get_movie_data_from_ombd(title='test'), {})
        request_get_mocked.assert_called_once_with(url='http://www.omdbapi.com/?apikey={}&t={}'.format('123', 'test'))
        logger_mocked.error.assert_called_once_with('Service was unavailable at the time')

    @mock.patch('movies.helpers.OMDB_API_TOKEN', '456')
    @responses.activate
    def test_return_in_correct_format(self):
        responses.add(responses.GET, 'http://www.omdbapi.com/?apikey={}&t={}'.format('456', 'test'),
                      json={
                          "UPPER_CASE_KEY": "value",
                          "lower_case_key": "value"
                      }, status=200)

        expected_result = {'upper_case_key': 'value', 'lower_case_key': 'value'}
        self.assertEqual(get_movie_data_from_ombd(title='test'), expected_result)
        self.assertEqual(responses.calls[0].request.url, 'http://www.omdbapi.com/?apikey={}&t={}'.format('456', 'test'))
