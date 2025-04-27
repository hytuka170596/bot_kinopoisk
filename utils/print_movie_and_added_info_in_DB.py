from peewee import IntegrityError
from model.UserForKinopoisk import HistoryRequest, User, Movie
from datetime import datetime
from config_data.config import DATE_FORMAT


def add_movie_to_history_requests(
    user: User, movie: Movie, history_request_limit: int = 15
) -> None:
    """Функция принимает пользователя, фильм или сериал и добавляет в базу данных информацию о фильме или сериале.
    Так же важно помнить, что если превысить лимит записей в бд(15 по умолчанию),
    то самая первая запись сотрётся."""
    try:
        if check_movie_exists(user, movie):
            return

        if (
            HistoryRequest.select().where(HistoryRequest.user == user).count()
            >= history_request_limit
        ):

            oldest_request = (
                HistoryRequest.select()
                .where(HistoryRequest.user == user)
                .order_by(HistoryRequest.search_date.asc())
                .first()
            )
            oldest_request.delete_instance()

        formatted_date = datetime.now().strftime(DATE_FORMAT)

        new_request = HistoryRequest(
            user=user,
            search_date=formatted_date,
            kinopoisk_id=movie.id,
            movie_name=movie.name_film,
            description=movie.description,
            rating=movie.rating_kp,
            year=movie.year,
            genre=movie.genres,
            age_rating=movie.age_rating,
            poster=movie.poster,
            viewed=False,
        )
        new_request.save()
        user.save()
    except IntegrityError:
        pass


def check_movie_exists(user: User, movie: Movie) -> bool:
    """Проверяет, существует ли фильм в истории запросов для пользователя."""

    return (
        HistoryRequest.select()
        .where(
            (HistoryRequest.user == user) & (HistoryRequest.kinopoisk_id == movie.id)
        )
        .exists()
    )
