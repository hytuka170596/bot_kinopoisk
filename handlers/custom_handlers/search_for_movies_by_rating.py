# coding=utf-8
from loader import bot
from telebot.types import Message, CallbackQuery
from state.movie_search import MovieStateInfo
from api.ApiKinopoisk import get_list_movies_by_rating
from model.UserForKinopoisk import Movie, User
from keyboards.inline.Kinopoisk_Keyboard import (
    keyboard_menu_or_reply,
    keyboard_with_ratings,
    keyboard_with_get_value_limit,
    keyboard_by_genre,
)
from utils.print_movie_and_added_info_in_DB import add_movie_to_history_requests
import re
from ExceptionsKP.KinopoiskERROR import NotFoundMovie


def is_valid_rating(rating: str) -> bool:
    try:
        if "-" in rating:
            first_num, second_num = map(float, rating.split("-"))
            return 0 <= first_num <= 10 and 0 <= second_num <= 10 and first_num <= second_num
        else:
            rating_float = float(rating)
            return 0 <= rating_float <= 10
    except ValueError:
        return False


@bot.callback_query_handler(func=lambda call: call.data == "rating")
def get_rating_from_user(call: CallbackQuery) -> None:
    bot.set_state(
        user_id=call.from_user.id,
        state=MovieStateInfo.get_movies_by_rating,)
    bot.send_message(
        chat_id=call.from_user.id,
        text="Выберете рейтинг для поиска или напишите цифрами в формате: 5.2 или 7 или 5.2 - 8",
        reply_markup=keyboard_with_ratings(),
    )


@bot.message_handler(commands=["movie_by_rating"])
def get_rating_from_user_command(message: Message) -> None:
    bot.set_state(
        user_id=message.from_user.id,
        state=MovieStateInfo.get_movies_by_rating,)
    bot.send_message(
        chat_id=message.from_user.id,
        text="Выберете рейтинг для поиска или напишите цифрами в формате: 5.2 или 7 или 5.2 - 8",
        reply_markup=keyboard_with_ratings(),
    )


@bot.message_handler(state=MovieStateInfo.get_movies_by_rating)
def get_by_rating(message: Message) -> None:
    rating_from_the_user = message.text.strip()
    rating_pattern = re.compile(r"^\d+(\.\d+)?(-\d+(\.\d+)?)?$")

    if rating_pattern.match(rating_from_the_user) and is_valid_rating(rating_from_the_user):
        user_id_for_telegram = message.from_user.id
        with bot.retrieve_data(user_id_for_telegram) as info_by_rating:
            info_by_rating["rating"] = rating_from_the_user

        bot.set_state(user_id=message.from_user.id, state=MovieStateInfo.get_movie_count_1)
        bot.send_message(
            chat_id=message.from_user.id,
            text="Выберете сколько фильмов вывести или напишите цифрой",
            reply_markup=keyboard_with_get_value_limit()
        )
    else:
        bot.send_message(
            chat_id=message.from_user.id,
            text="Некорректный формат рейтинга. "
                 "\nПожалуйста, введите рейтинг в формате: 5.2 или 7 или 5.2 - 8 и убедитесь, что рейтинг находится"
                 " в диапазоне от 0 до 10.",
        )


@bot.callback_query_handler(func=lambda call: True, state=MovieStateInfo.get_movies_by_rating)
def get_film_list_by_rating(call: CallbackQuery) -> None:
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    rating_from_the_user = call.data
    if is_valid_rating(rating_from_the_user):
        user_id_for_telegram = call.from_user.id
        with bot.retrieve_data(user_id_for_telegram) as info_by_rating:
            info_by_rating["rating"] = rating_from_the_user

        bot.set_state(user_id=call.from_user.id, state=MovieStateInfo.get_movie_count_1)
        bot.send_message(
            chat_id=call.from_user.id,
            text="Выберете сколько фильмов вывести или напишите цифрой",
            reply_markup=keyboard_with_get_value_limit()
        )
    else:
        bot.send_message(
            call.from_user.id,
            "Попробуйте ещё раз,\nВы некорректно указали рейтинг для поиска. "
            "Убедитесь, что рейтинг находится в диапазоне от 0 до 10.",
        )


@bot.message_handler(state=MovieStateInfo.get_movie_count_1)
@bot.callback_query_handler(func=lambda call: True, state=MovieStateInfo.get_movie_count_1)
def get_movie_count(message_or_call: Message | CallbackQuery) -> None:
    if isinstance(message_or_call, CallbackQuery):
        user_id_for_telegram = message_or_call.from_user.id
        bot.edit_message_reply_markup(
            chat_id=user_id_for_telegram, message_id=message_or_call.message.message_id
        )
        bot.delete_message(chat_id=user_id_for_telegram, message_id=message_or_call.message.message_id-1)
        movie_count = int(message_or_call.data)
    else:
        user_id_for_telegram = message_or_call.from_user.id
        movie_count = int(message_or_call.text.strip())
    try:
        if movie_count <= 0:
            raise ValueError("Количество фильмов должно быть больше нуля.")

        with bot.retrieve_data(user_id_for_telegram) as info_by_rating:
            info_by_rating["limit"] = movie_count

        bot.set_state(user_id_for_telegram, state=MovieStateInfo.added_genre)
        bot.send_message(user_id_for_telegram,
                         "Выберете жанр", reply_markup=keyboard_by_genre())

    except ValueError as exc:
        bot.send_message(
            chat_id=user_id_for_telegram,
            text=f"Некорректное значение: {exc}. Пожалуйста, введите число.",
        )


@bot.message_handler(state=MovieStateInfo.added_genre)
@bot.callback_query_handler(func=lambda call: True, state=MovieStateInfo.added_genre)
def get_genres(message_or_call: Message | CallbackQuery) -> None:
    user_id_for_telegram = message_or_call.from_user.id
    if isinstance(message_or_call, CallbackQuery):
        bot.edit_message_reply_markup(
            chat_id=user_id_for_telegram, message_id=message_or_call.message.message_id
        )
        bot.delete_message(chat_id=user_id_for_telegram, message_id=message_or_call.message.message_id-1)
        genre = message_or_call.data
        if genre == "stop":
            bot.delete_message(chat_id=user_id_for_telegram, message_id=message_or_call.message.message_id)
            finalize_genre_selection(user_id_for_telegram)
            return
    else:
        genre = message_or_call.text.strip()
        genres = extract_genres_from_message(genre)
        if "stop" in genres:

            finalize_genre_selection(user_id_for_telegram)
            return

    with bot.retrieve_data(user_id_for_telegram) as info_by_rating:
        if "genres" not in info_by_rating:
            info_by_rating["genres"] = []
        if isinstance(message_or_call, CallbackQuery):
            info_by_rating["genres"].append(genre)
        else:
            info_by_rating["genres"].extend(genres)

    if isinstance(message_or_call, Message):
        bot.send_message(user_id_for_telegram,
                         "Выберите еще один жанр или введите \"Показать подборку\" для завершения выбора:",
                         reply_markup=keyboard_by_genre())
    else:
        bot.send_message(user_id_for_telegram,
                         "Выберите еще один жанр или нажмите \"Показать подборку\" для завершения выбора:",
                         reply_markup=keyboard_by_genre())


def finalize_genre_selection(user_id_for_telegram: int) -> None:
    with bot.retrieve_data(user_id_for_telegram) as info_by_rating:
        genres = info_by_rating.get("genres", [])
        rating = info_by_rating.get("rating")
        limit_value = info_by_rating.get("limit")

    try:
        movies_list = get_list_movies_by_rating(
            rating=rating, limit=int(limit_value), genre=genres)
        user = User.get_or_none(User.telegram_id == user_id_for_telegram)
        if movies_list is not None:
            for i_movie in movies_list:
                movie = Movie(i_movie)
                bot.send_photo(user_id_for_telegram, movie.poster)
                bot.send_message(user_id_for_telegram, movie)

                add_movie_to_history_requests(user=user, movie=movie)

            call_text = "rating"

            bot.send_message(
                chat_id=user_id_for_telegram,
                text="Что делаем дальше?",
                reply_markup=keyboard_menu_or_reply(call_text),
            )
            bot.delete_state(user_id_for_telegram)

        else:
            bot.send_message(user_id_for_telegram, "Возникла ошибка.")

    except NotFoundMovie as exc:
        bot.send_message(user_id_for_telegram, text=exc)


def extract_genres_from_message(text: str) -> list:
    separators = [',', ' ', ';']
    for sep in separators:
        if sep in text:
            return [genre.strip() for genre in text.split(sep) if genre.strip()]
    return [text]
