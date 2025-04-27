# coding=utf-8
from peewee import (
    DateField,
    CharField,
    TextField,
    BooleanField,
    ForeignKeyField,
    IntegerField,
    Model,
)

from database.movie_database import MOVIE_DB
from config_data.config import DATE_FORMAT

foto = (
    "https://yandex.ru/images/search?img_url=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F05%2F80%2F4a%2F05804a3440c4f338cf"
    "22052378a3d2f3.jpg&lr=51&nl=1&pos=0&rpt=simage&source=morda&source-serpid=NQihA9ELiSOIv7Nl2gR2uA&text=%D0%A1%D0%B0"
    "%D0%BC%D1%8B%D0%B5%20%D0%BC%D0%B8%D0%BB%D1%8B%"
    "D0%B5%20%D0%B6%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5"
)
NOT_FOUND_INFO = "NO INFO"


class BaseModel(Model):
    """Базовая модель связывающая всех своих наследников к одной базе данных,
    создавая для них свои таблицы с указанными атрибутами.
    Модель построена на библиотеке << peewee >>."""

    class Meta:
        """
        Клас мета прописывает дополнительные характеристики, которые будут необходимы.
        Например, название таблицы, сортировка по какому-то атрибуту и т.п.
        В данном случае даёт ссылку на рабочую базу данных.
        """

        database = MOVIE_DB


class User(BaseModel):
    """Класс Пользователь телеграм бота."""

    class Meta:
        """
        Клас мета прописывает дополнительные характеристики, которые будут необходимы.
        Например, название таблицы, сортировка по какому-то атрибуту и т.п.
        """

        db_table = "Users"

    telegram_id = IntegerField(unique=True)
    username = CharField()
    first_name = CharField()
    last_name = CharField(null=True)


class HistoryRequest(BaseModel):
    """История запросов пользователя"""

    class Meta:
        """
        Клас мета прописывает дополнительные характеристики, которые будут необходимы.
        Например, название таблицы, сортировка по какому-то атрибуту и т.п.
        """

        db_table = "HistoryRequests"

    user = ForeignKeyField(User, backref="history_requests")
    search_date = DateField(null=True)
    kinopoisk_id = CharField(null=True)
    movie_name = CharField(null=True)
    description = TextField(null=True)
    rating = CharField(null=True)
    year = CharField(null=True)
    genre = CharField(null=True)
    age_rating = CharField(null=True)
    poster = CharField(null=True)
    viewed = BooleanField(default=False)

    def __str__(self) -> str:
        """Возвращает строковое представление истории запроса."""
        return (
            f"Дата поиска: {self.search_date}\n"
            f"ID на кинопоиске: {self.kinopoisk_id}\n"
            f"Название фильма: {self.movie_name}\n"
            f"Рейтинг: {self.rating}\n"
            f"Год выхода: {self.year}\n"
            f"Жанр: {self.genre}\n"
            f"Возрастной рейтинг: {self.age_rating}+\n"
            f"\nОписание:\n {self.description}\n"
            f"{self.checkout_view()}\n"
        )

    def checkout_view(self) -> str:
        """Проверка просмотрен фильм или нет."""
        answer = "\n\n{}   -  не просмотрен!".format(self.movie_name)
        if self.viewed:
            answer = "Просмотрено."

        return answer

    def update_viewed(self) -> None:
        """Обновляет поле viewed на True, если фильм был просмотрен."""
        self.viewed = True
        self.save()


class Movie(BaseModel):
    """
    Класс для создания информации о фильме или сериале.
    В случае отсутствие атрибута, он заменяется константой NO_INFO
    """

    def __init__(self, data: dict, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.id = data.get("id", NOT_FOUND_INFO)
        self.name_film = (
            data.get("name") or data.get("alternativeName") or NOT_FOUND_INFO
        )
        self.year = data.get("year", NOT_FOUND_INFO)
        self.description = data.get("description", NOT_FOUND_INFO)
        self.genres = ", ".join(genre["name"] for genre in data.get("genres", []))
        self.rating_kp = data.get("rating", {}).get("kp", NOT_FOUND_INFO)
        self.rating_imdb = data.get("rating", {}).get("imdb", NOT_FOUND_INFO)
        self.length_film = data.get("movieLength", NOT_FOUND_INFO)
        self.length_series = data.get("seriesLength", NOT_FOUND_INFO)
        self.countries = ", ".join(
            country["name"] for country in data.get("countries", [])
        )
        self.age_rating = data.get("ageRating", NOT_FOUND_INFO)
        self.budget = data.get("budget", {}).get("value", NOT_FOUND_INFO)
        self.currency = data.get("budget", {}).get("currency", NOT_FOUND_INFO)
        self.check_serial = data.get("isSeries", False)
        self.type = data.get("type", NOT_FOUND_INFO)
        self.poster = data.get("poster", {}).get("url") or foto
        self.trailer = data.get("trailers", {}).get("url", NOT_FOUND_INFO)

    def __str__(self) -> str:
        """Проверяет все детали, и возвращает корректную информацию о фильме"""
        details = [
            f"ID фильма на кинопоиске: {self.id}",
            f"Тип кино: {self.type_mapping()}",
            f"Название фильма: {self.name_film}",
            f"Год выхода: {self.year}",
            f"Жанр: {self.genres}",
            f"Рейтинг на кинопоиске: {self.rating_kp}",
            f"Рейтинг на IMDB: {self.rating_imdb}",
            self.film_duration(),
            f"Страна создатель: {self.countries}",
            f"Возрастной рейтинг: {self.age_rating}{self.checkout_age_rating()}",
            self.budget_details(),
            f"\nОписание:\n{self.description}\n",
        ]
        return "\n".join(filter(None, details))

    def film_duration(self) -> str:
        """Возвращает строку о продолжительности фильма или серии."""
        if self.check_serial:
            return (
                f"Продолжительность серии: {self.length_series} мин."
                if self.length_series != NOT_FOUND_INFO
                else "Продолжительность серии: NO INFO"
            )
        return (
            f"Продолжительность фильма: {self.length_film} мин."
            if self.length_film != NOT_FOUND_INFO
            else "Продолжительность фильма: NO INFO"
        )

    def budget_details(self) -> str:
        """Возвращает строку с деталями бюджета, если они доступны."""
        if self.budget != NOT_FOUND_INFO and self.currency != NOT_FOUND_INFO:
            return f"Бюджет: {self.budget} {self.currency}"
        return ""

    def type_mapping(self) -> str:
        """Преобразует тип кино в читаемый формат."""
        type_mapping = {
            "movie": "Фильм",
            "tv-series": "ТВ-Сериал",
            "animated-series": "Анимационный-сериал",
            "anime": "Аниме",
            "cartoon": "Мультфильм",
        }
        return type_mapping.get(self.type, self.type)

    def checkout_age_rating(self) -> str:
        """Проверяет возрастной рейтинг и возвращает знак '+' если это число."""
        return "+" if isinstance(self.age_rating, int) else ""


def create_model():
    """
    Функция создаёт все таблицы со всеми атрибутами для всех моделей унаследованных от BaseModel
    """
    MOVIE_DB.create_tables(BaseModel.__subclasses__())
