import copy
import re
import urllib.parse
from datetime import datetime

from log import logger
from notification import mail_client
from service.http_request import http_get

# Made up of tuple of movie_url, date and email
# example : (
#   "https://in.bookmyshow.com/buytickets/spider-man-no-way-home-patna/movie-patn-ET00319080-MT/20211216",
#   "20211216",
#   "chaudhary.kc.kunal@gmail.com"
# )
BS_MONITORS = []


def add_monitor_for_booking_started_movies(url: str, date: str, email: str) -> None:
    logger().info("adding to booking started monitor: %s", str((url, date, email)))
    validate_url(url)
    validate_date(date)
    validate_email(email)
    BS_MONITORS.append((url, date, email))
    logger().info("added to booking started monitor: %s", str((url, date, email)))


def validate_url(url: str) -> None:
    url_split = urllib.parse.urlsplit(url)
    if url_split.scheme is None or url_split.netloc is None:
        raise ValueError("invalid url")
    # last part of path is a date for booking started movies
    try:
        validate_date(url_split.path.split("/")[-1])
    except Exception:
        raise ValueError("Invalid url - does not end with date like 20210131")


def validate_date(date: str) -> None:
    if len(date) != 8:
        raise ValueError("length of date should be 8. Example : 20210131")
    datetime(year=int(date[0:4]), month=int(date[4:6]), day=int(date[6:8]))


def validate_email(email: str) -> None:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, email):
        raise ValueError("invalid email")


def monitor_booking_started_movies() -> None:
    monitors = copy.deepcopy(BS_MONITORS)
    while len(monitors) > 0:
        entry = monitors.pop()
        logger().info("checking entry : %s", str(entry))
        # Double check to eliminate false positives
        if check_booking_started(movie_url=entry[0], target_date=entry[1]):
            if check_booking_started(movie_url=entry[0], target_date=entry[1]):
                logger().info("removing entry: %s", str(entry))
                BS_MONITORS.remove(entry)
                send_email(email=entry[2], movie_url=entry[0], date=entry[1])


def check_booking_started(movie_url: str, target_date: str) -> bool:
    validate_url(url=movie_url)
    validate_date(date=target_date)
    response_date = fetch_response_date(movie_url, target_date)
    logger().info("target_date=%s, response_date=%s", str(target_date), str(response_date))
    response_datetime = datetime(
        year=int(response_date[0:4]),
        month=int(response_date[4:6]),
        day=int(response_date[6:8]))
    target_datetime = datetime(
        year=int(target_date[0:4]),
        month=int(target_date[4:6]),
        day=int(target_date[6:8]))
    return target_datetime <= response_datetime


def fetch_response_date(movie_url: str, target_date: str) -> str:
    target_url = get_target_url(orig_url=movie_url, target_date=target_date)
    bms_response = http_get(target_url)
    logger().info("target url=%s, bms_response_url=%s", target_url, bms_response.url)
    return response_date_from_url(bms_response.url)


# replaces original date with target date in the original url
def get_target_url(orig_url: str, target_date: str) -> str:
    target_url_path_split = urllib.parse.urlsplit(orig_url).path.split("/")
    target_url_path_split[-1] = target_date
    target_url_path = "/".join(target_url_path_split)
    return urllib.parse.urlsplit(orig_url)._replace(path=target_url_path).geturl()


def response_date_from_url(response_url: str) -> str:
    date = urllib.parse.urlsplit(response_url).path.split("/")[-1]
    validate_date(date)
    return date


def send_email(email: str, movie_url: str, date: str) -> None:
    logger().info("Sending email. movie=%s, date=%s, email=%s", movie_url, date, email)
    mail_client.send_mail(
        subject="Booking Started for movie",
        content="Movie url: {} \n Target Booking Date : {}".format(movie_url, date),
        receivers=[email])
