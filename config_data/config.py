import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env.template")
else:
    load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
TOKEN_KINOPOISK = os.getenv("TOKEN_KINOPOISK")
DATE_FORMAT = "%d.%m.%Y"
API_KINOPOISK_BY_NAME = os.getenv("API_KINOPOISK_BY_NAME")
API_KINOPOISK_BY_FILTER = os.getenv("API_KINOPOISK_BY_FILTER")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("movie_search", "Поиск фильма/сериала по названию"),
    ("movie_by_rating", "Поиск фильмов/сериалов по рейтингу"),
    ("low_budget_movie", "Поиск фильмов/сериалов с низким бюджетом"),
    ("high_budget_movie", "Поиск фильмов/сериалов с высоким бюджетом"),
    ("history", "История запросов и поиска фильма/сериала."),
)
