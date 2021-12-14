import atexit
import logging.config
from http import HTTPStatus

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request

from config import APP_NAME
from log import get_log_config
from service import *

logging.config.dictConfig(get_log_config())
app = Flask(APP_NAME)


@app.route('/status', methods=['GET'])
def health_check():
    return {"status": "UP"}, HTTPStatus.OK


@app.route('/movies/list/<city>', methods=['GET'])
def movies_for_city(city: str):
    try:
        movies = get_movie_names_for_city(city)
        return {"city": city, "movies": movies}, HTTPStatus.OK
    except Exception as error:
        return {"city": city, "error": str(error)}, HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/movies/booking/status', methods=['POST'])
def check_booking_status():
    try:
        movie_url = str(request.json['url'])
        target_date = str(request.json['date'])
        booking_status = check_booking_started(movie_url=movie_url, target_date=target_date)
        return {"url": movie_url, "date": target_date, "booking": booking_status}, HTTPStatus.OK
    except KeyError as error:
        return {"error": str(error)}, HTTPStatus.BAD_REQUEST
    except ValueError as error:
        return {"error": str(error)}, HTTPStatus.BAD_REQUEST
    except Exception as error:
        return {"error": str(error)}, HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/movies/monitor/booking-started', methods=['POST'])
def monitor_booking_status():
    try:
        movie_url = str(request.json['url'])
        target_date = str(request.json['date'])
        email = str(request.json['email'])
        add_monitor_for_booking_started_movies(url=movie_url, date=target_date, email=email)
        return {"success": True}, HTTPStatus.OK
    except KeyError as error:
        return {"error": str(error)}, HTTPStatus.BAD_REQUEST
    except ValueError as error:
        return {"error": str(error)}, HTTPStatus.BAD_REQUEST
    except Exception as error:
        return {"error": str(error)}, HTTPStatus.INTERNAL_SERVER_ERROR


# TODO: /monitor/upcoming/<city>/<movie>?email=?

scheduler = BackgroundScheduler()
scheduler.add_job(func=monitor_booking_started_movies, trigger="interval", seconds=120)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
