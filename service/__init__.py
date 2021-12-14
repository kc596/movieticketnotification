from service.movies_for_city import get_movie_urls_for_city


def get_movie_urls(city: str) -> list:
    return get_movie_urls_for_city(city)
