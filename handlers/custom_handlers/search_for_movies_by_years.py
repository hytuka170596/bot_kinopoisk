# coding=utf-8
from loader import bot
from telebot.types import Message, CallbackQuery
from state.movie_search import MovieStateInfo
from api.ApiKinopoisk import get_list_movies_by_year
from model.UserForKinopoisk import Movie, User
from ExceptionsKP.KinopoiskERROR import NotFoundMovie, ErrorCurrentYearKP
from keyboards.inline.Kinopoisk_Keyboard import (
    keyboard_menu_or_reply,
    keyboard_with_years,
)
from utils.print_movie_and_added_info_in_DB import add_movie_to_history_requests


@bot.callback_query_handler(func=lambda call: call.data == "year")
def make_keyboard_date(call: CallbackQuery) -> None:
    bot.set_state(call.from_user.id, state=MovieStateInfo.get_year_for_user)

    with bot.retrieve_data(call.from_user.id) as info_for_keyboard:
        info_for_keyboard["callback_text"] = call.data

    if call.data == "year":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберете дату или напишите самостоятельно.",
            reply_markup=keyboard_with_years(),
        )


@bot.callback_query_handler(
    state=MovieStateInfo.get_year_for_user,
    func=lambda call: call.data.endswith("-year"),
)
def handler_year_for_user(call: CallbackQuery) -> None:
    year, _ = call.data.split("-")
    try:
        if len(year) == 4 and year.isdigit():
            curr_year = year

            with bot.retrieve_data(call.from_user.id) as info_for_search_by_year:
                info_for_search_by_year["year"] = curr_year

        else:
            raise ErrorCurrentYearKP

        bot.send_message(
            call.from_user.id, "Теперь напиши, сколько подходящих вариантов вывести?"
        )
        bot.set_state(call.from_user.id, state=MovieStateInfo.get_limit_movie)

    except ErrorCurrentYearKP as exc:
        bot.send_message(call.from_user.id, text=f"{exc}")


@bot.message_handler(state=MovieStateInfo.get_limit_movie)
def return_film_by_year(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(
            user_id=message.from_user.id, chat_id=message.from_user.id
        ) as data_for_movie:
            data_for_movie["limit"] = message.text

        limit_value = data_for_movie["limit"]

        with bot.retrieve_data(message.from_user.id) as info_for_search_by_year:
            curr_year = info_for_search_by_year["year"]

        try:
            movies_list = get_list_movies_by_year(
                year=curr_year, limit=int(limit_value)
            )
            user_id_for_telegram = message.from_user.id
            user = User.get_or_none(User.telegram_id == user_id_for_telegram)
            if movies_list is not None:
                for i_movie in movies_list:
                    movie = Movie(i_movie)
                    bot.send_photo(message.chat.id, movie.poster)
                    bot.send_message(message.chat.id, movie)

                    add_movie_to_history_requests(user=user, movie=movie)

                with bot.retrieve_data(message.from_user.id) as info_for_keyboard:
                    call_text = info_for_keyboard["callback_text"]

                bot.send_message(
                    chat_id=message.from_user.id,
                    text="Что делаем дальше?",
                    reply_markup=keyboard_menu_or_reply(call_text),
                )

            else:
                bot.send_message(message.from_user.id, "Возникла ошибка.")

        except NotFoundMovie as exc:
            bot.send_message(message.chat.id, text=exc)

        finally:
            bot.delete_state(message.from_user.id, message.chat.id)

    else:
        bot.send_message(
            message.from_user.id,
            "Цифрой напишите, максимальное кол-во выводимых результатов подходящих под запрос",
        )
