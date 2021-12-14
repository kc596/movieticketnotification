import logging.config
from http import HTTPStatus

from flask import Flask

from config import APP_NAME
from log import get_log_config
from service import get_movie_urls

logging.config.dictConfig(get_log_config())
app = Flask(APP_NAME)


@app.route('/status', methods=['GET'])
def health_check():
    return {"status": "UP"}, HTTPStatus.OK


@app.route('/movies/list/<city>', methods=['GET'])
def movies_for_city(city: str):
    try:
        movies = get_movie_urls(city)
        return {"city": city, "movies": movies}, HTTPStatus.OK
    except Exception as error:
        return {"city": city, "error": error}, HTTPStatus.INTERNAL_SERVER_ERROR


"""
/monitor/upcoming/<city>/<movie>?email=?
"""

"""
/monitor/released/<movie-url>?email=?&date=?
"""
