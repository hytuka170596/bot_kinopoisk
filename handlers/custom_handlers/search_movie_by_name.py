# coding=utf-8
from requests.exceptions import ConnectionError
from telebot.types import Message, CallbackQuery
from api.ApiKinopoisk import get_film_by_name
from keyboards.inline.Kinopoisk_Keyboard import keyboard_menu_or_reply, menu_main
from loader import bot
from model.UserForKinopoisk import Movie, User
from state.movie_search import MovieStateInfo
from utils.print_movie_and_added_info_in_DB import add_movie_to_history_requests


@bot.message_handler(commands=["movie_search"])
def search_film(message: Message) -> None:
    bot.set_state(message.from_user.id, state=MovieStateInfo.get_name_movie)
    bot.send_message(message.from_user.id, "Напиши название фильма")


@bot.callback_query_handler(func=lambda call: call.data == "movie_search")
def callback_movie_search(call: CallbackQuery):
    bot.set_state(call.from_user.id, state=MovieStateInfo.get_name_movie)
    if call.data == "movie_search":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Напиши название фильма",
        )
    with bot.retrieve_data(call.from_user.id) as info_for_keyboard:
        info_for_keyboard["callback_text"] = call.data


@bot.message_handler(state=MovieStateInfo.get_name_movie)
def get_name_film(message: Message):

    bot.send_message(
        message.from_user.id, "Теперь напиши, сколько подходящих вариантов вывести?"
    )
    bot.set_state(message.from_user.id, state=MovieStateInfo.get_limit_movies)
    with bot.retrieve_data(message.from_user.id) as data_for_movie:
        data_for_movie["name"] = message.text

    with bot.retrieve_data(message.from_user.id) as info_for_keyboard:
        info_for_keyboard["callback_text"] = "movie_search"


@bot.message_handler(state=MovieStateInfo.get_limit_movies)
def return_film(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(
            user_id=message.from_user.id, chat_id=message.from_user.id
        ) as data_for_movie:
            data_for_movie["limit"] = message.text
        name_movie = data_for_movie["name"]
        limit_value = data_for_movie["limit"]

        try:
            movies_list = get_film_by_name(name=name_movie, limit=limit_value)
            user_id_for_telegram = message.from_user.id
            user = User.get_or_none(User.telegram_id == user_id_for_telegram)
            if movies_list is not None:
                for i_movie in movies_list:
                    movie = Movie(i_movie)
                    bot.send_photo(message.chat.id, movie.poster)
                    bot.send_message(message.chat.id, movie)
                    add_movie_to_history_requests(user=user, movie=movie)

            else:
                bot.send_message(message.chat.id, text="Фильм не найден на сайте")

            bot.send_message(
                chat_id=message.from_user.id,
                text="Что делаем дальше?",
                reply_markup=keyboard_menu_or_reply(data_for_movie["callback_text"]),
            )

        except ConnectionError as exc:
            bot.send_message(message.chat.id, text=str(exc))
        finally:
            bot.delete_state(message.from_user.id)

    else:
        bot.send_message(
            message.from_user.id,
            "Цифрой напишите, максимальное кол-во выводимых результатов подходящих под запрос",
        )


@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def callback_menu(call: CallbackQuery) -> None:
    bot.delete_state(user_id=call.message.from_user.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🌆🌁🌉🌄🌅🏞🎑🏙    Главное меню    👀👀👀",
        reply_markup=menu_main(),
    )
