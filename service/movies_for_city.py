import json
from json.decoder import JSONDecodeError

from lxml import html

from config import *
from log import logger
from service.http_request import http_get


##########################################################################
# Find all javascript on page which are json,
# and parse all urls starting with in.bookmyshow.com/city/movies/<movie>
##########################################################################
def get_movie_urls_for_city(city: str) -> list:
    script_elements = fetch_script_elements(city)
    return collect_movie_urls_in_scripts(script_elements, city)


def fetch_script_elements(city: str) -> list:
    bms_response = http_get("https://{}/{}/{}".format(BMS_HOST, city, BMS_PATH_MOVIES))
    html_element = html.fromstring(bms_response)
    return html_element.findall('.//script')


def collect_movie_urls_in_scripts(script_elements: list, city: str) -> list:
    result = set()
    logger().info("collecting movie urls in %d scripts", len(script_elements))
    for script_element in script_elements:
        collect_movie_urls_in_script(
            script_txt=script_element.text,
            city=city,
            result=result)
    return list(result)


def collect_movie_urls_in_script(script_txt: str, city: str, result: set) -> None:
    json_script = filter_json_script(script_txt)
    collect_movie_urls_in_json_obj(obj=json_script, city=city, result=result)
    logger().info("Total %d movie urls found", len(result))


def filter_json_script(script_txt):
    logger().info("Converting script to json")
    try:
        return json.loads(script_txt)
    except JSONDecodeError as err:
        pass  # json decode error, do nothing
    except TypeError as err:
        pass  # json decode error, do nothing
    logger().info("The script could not be converted to json")
    return None


def collect_movie_urls_in_json_obj(obj, city: str, result: set) -> None:
    if obj is None:
        return
    if isinstance(obj, list):
        logger().info("collecting movie urls in json list")
        for key in obj:
            collect_movie_urls(obj=key, city=city, result=result)
    if isinstance(obj, dict):
        logger().info("collecting movie urls in json dict")
        for key in obj:
            collect_movie_urls(obj=obj[key], city=city, result=result)


def collect_movie_urls(obj, city: str, result: set) -> None:
    if isinstance(obj, str):
        if str_contains_movie_url(url=obj, city=city):
            logger().info("Found a valid movie url : %s", obj)
            result.add(obj)
    if isinstance(obj, list):
        for item in obj:
            collect_movie_urls(obj=item, city=city, result=result)
    if isinstance(obj, dict):
        for k, v in obj.items():
            collect_movie_urls(obj=v, city=city, result=result)


def str_contains_movie_url(url: str, city: str) -> bool:
    return "{}/{}/{}".format(BMS_HOST, city, BMS_PATH_MOVIES) in url
