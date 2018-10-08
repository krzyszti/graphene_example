import logging

import requests

from graph_test.settings import OMDB_API_TOKEN

logger = logging.getLogger(__name__)

URL_TEMPLATE = 'http://www.omdbapi.com/?apikey={}&t={}'


def get_movie_data_from_ombd(title):
    try:
        response = requests.get(url=URL_TEMPLATE.format(OMDB_API_TOKEN, '+'.join(title.split())))
    except ConnectionError:
        logger.error('Service was unavailable at the time')
        return {}
    else:
        return {key.lower(): value for key, value in response.json().items()}
