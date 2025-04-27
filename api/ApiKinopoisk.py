# coding=utf-8
import json
import requests
from requests.exceptions import ConnectionError
from ExceptionsKP.KinopoiskERROR import RequestErrorLimit
from config_data.config import (
    TOKEN_KINOPOISK,
    API_KINOPOISK_BY_NAME,
    API_KINOPOISK_BY_FILTER,
)
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("error_api.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

__header = {
    "accept": "application/json",
    "X-API-KEY": TOKEN_KINOPOISK,
}


def get_film_by_name(name: str, limit: int = 1, page: int = 1) -> dict | None:
    """
    Поиск фильмов по названию
    :param name: название фильма
    :param limit: максимальное кол-во подходящих фильмов подходящих под запрос
    :param page: номер страницы
    :return: вернётся словарь с данными о фильме, либо None если ничего не найдётся
    """

    try:
        response = requests.get(
            url=API_KINOPOISK_BY_NAME,
            params={
                "query": name,
                "limit": limit,
                "page": page,
            },
            headers=__header,
        )
        if response.status_code == 200:
            movie = json.loads(response.text)
            if movie["docs"]:
                return movie["docs"]
            else:
                return
        elif response.status_code == 403:
            logger.error(RequestErrorLimit)
            raise RequestErrorLimit
        else:
            logger.error(f"Ошибка: Неожиданный статус-код {response.status_code}")
            return

    except ConnectionError as exc:
        logger.error(f"Ошибка подключения: {exc}")
        return


def get_list_movies_by_rating(
    rating: str, page: int = 1, limit: int = 5, genre: list | str | None = None
) -> dict | None:
    """
    Поиск фильмов по рейтингу
    :param rating: рейтинг по которому будет идти поиск
    :param limit: максимальное кол-во подходящих фильмов подходящих под запрос
    :param page: номер страницы
    :param genre: жанр или список жанров
    :return: вернётся словарь с данными о фильме, либо None если ничего не найдётся
    """

    try:
        response = requests.get(
            url=API_KINOPOISK_BY_FILTER,
            params={
                "selectFields": [
                    "type",
                    "id",
                    "name",
                    "description",
                    "isSeries",
                    "year",
                    "rating",
                    "ageRating",
                    "votes",
                    "movieLength",
                    "genres",
                    "countries",
                    "poster",
                    "videos",
                ],
                "notNullFields": [
                    "type",
                    "id",
                    "name",
                    "description",
                    "isSeries",
                    "year",
                    "rating.kp",
                    "ageRating",
                    "genres.name",
                    "countries.name",
                    "poster.url",
                    "videos.trailers.url",
                ],
                "sortField": "rating.kp",
                "sortType": "-1",
                "rating.kp": rating,
                "limit": limit,
                "page": page,
                "genres": [genre]
            },
            headers=__header,
        )
        if response.status_code == 200:
            movies = response.json()
            return movies["docs"]
        elif response.status_code == 403:
            logger.error(RequestErrorLimit)
            raise RequestErrorLimit
        else:
            logger.error(f"Ошибка: Неожиданный статус-код {response.status_code}")
            return
    except ConnectionError as exc:
        logger.error(f"Ошибка подключения: {exc}")
        return


def get_list_movies_by_year(year: str, page: int = 1, limit: int = 5) -> dict | None:
    """
    Поиск фильмов по годам
    :param year: год или период лет за который будет идти поиск
    :param limit: максимальное кол-во подходящих фильмов подходящих под запрос
    :param page: номер страницы
    :return: вернётся словарь с данными о фильме, либо None если ничего не найдётся
    """
    try:
        response = requests.get(
            url=API_KINOPOISK_BY_FILTER,
            params={
                "limit": limit,
                "page": page,
                "selectFields": [
                    "type",
                    "id",
                    "name",
                    "description",
                    "isSeries",
                    "year",
                    "rating",
                    "ageRating",
                    "votes",
                    "movieLength",
                    "genres",
                    "countries",
                    "poster",
                    "videos",
                ],
                "notNullFields": [
                    "type",
                    "id",
                    "name",
                    "description",
                    "isSeries",
                    "year",
                    "rating.kp",
                    "rating.imdb",
                    "ageRating",
                    "genres.name",
                    "countries.name",
                    "poster.url",
                    "videos.trailers.url",
                ],
                "sortField": "rating.kp",
                "sortType": "-1",
                "year": year,
            },
            headers=__header,
        )
        if response.status_code == 200:
            movies = response.json()
            return movies["docs"]
        elif response.status_code == 403:
            logger.error(RequestErrorLimit)
            raise RequestErrorLimit

        else:
            logger.error(f"Ошибка: Неожиданный статус-код {response.status_code}")
            return
    except ConnectionError as exc:
        logger.error(f"Ошибка подключения: {exc}")
        return


def get_list_movies_by_budget(
    flag_min_or_max: str,
    page: int = 1,
    limit: int = 5,
) -> dict | None:
    """
    Поиск фильмов по бюджету
    :param flag_min_or_max: флаг означающий за какой бюджет искать фильм мин. или макс.
    :param limit: максимальное кол-во подходящих фильмов подходящих под запрос
    :param page: номер страницы
    :return: вернётся словарь с данными о фильме, либо None если ничего не найдётся
    """
    flag = ""
    if flag_min_or_max == "low_budget_movie":
        flag = "1"
    elif flag_min_or_max == "high_budget_movie":
        flag = "-1"

    try:
        response = requests.get(
            url=API_KINOPOISK_BY_FILTER,
            params={
                "limit": limit,
                "page": page,
                "selectFields": [
                    "type",
                    "id",
                    "name",
                    "description",
                    "isSeries",
                    "year",
                    "rating",
                    "ageRating",
                    "movieLength",
                    "genres",
                    "countries",
                    "poster",
                    "budget",
                    "videos",
                ],
                "notNullFields": [
                    "budget.value",
                    "type",
                    "id",
                    "name",
                    "description",
                    "isSeries",
                    "year",
                    "rating.kp",
                    "rating.imdb",
                    "ageRating",
                    "genres.name",
                    "countries.name",
                    "poster.url",
                    "videos.trailers.url",
                ],
                "budget.value": "!0",
                "sortField": "budget.value",
                "sortType": flag,
            },
            headers=__header,
        )
        if response.status_code == 200:
            movies = response.json()
            return movies["docs"]
        elif response.status_code == 403:
            logger.error(RequestErrorLimit)
            raise RequestErrorLimit("Превышен лимит запросов")
        else:
            logger.error(f"Ошибка: Неожиданный статус-код {response.status_code}")
            return
    except ConnectionError as exc:
        logger.error(f"Ошибка подключения: {exc}")
        return
