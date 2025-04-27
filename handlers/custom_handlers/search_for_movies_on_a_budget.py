# coding=utf-8
from loader import bot
from telebot.types import Message, CallbackQuery
from keyboards.inline.Kinopoisk_Keyboard import (
    keyboard_with_get_value_limit,
    keyboard_menu_or_reply,
)
from api.ApiKinopoisk import get_list_movies_by_budget
from model.UserForKinopoisk import Movie, User, HistoryRequest
from ExceptionsKP.KinopoiskERROR import NotFoundMovie
from state.movie_search import MovieStateInfo
from utils.print_movie_and_added_info_in_DB import add_movie_to_history_requests


@bot.callback_query_handler(
    func=lambda call: call.data in ["low_budget_movie", "high_budget_movie"]
)
@bot.message_handler(commands=["low_budget_movie", "high_budget_movie"])
def get_the_request_limit(call: CallbackQuery = None, message: Message = None) -> None:
    user_id = call.from_user.id if call else message.from_user.id
    chat_id = call.message.chat.id if call else message.chat.id

    budget_type = call.data if call else message.text

    bot.set_state(user_id, state=MovieStateInfo.get_movies_by_budget)

    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as info_by_callback:
        info_by_callback["callback_text"] = budget_type

    if call:
        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=call.message.message_id,
            reply_markup=keyboard_with_get_value_limit(),
        )
    else:
        bot.send_message(
            chat_id=chat_id,
            text="Выберите лимит",
            reply_markup=keyboard_with_get_value_limit(),
        )


@bot.callback_query_handler(
    func=lambda call: True,
    state=MovieStateInfo.get_movies_by_budget,
)
def return_film_list(call: CallbackQuery) -> None:
    curr_limit = call.data

    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)

    with bot.retrieve_data(
        user_id=call.from_user.id, chat_id=call.message.chat.id
    ) as info_by_callback:
        flag = info_by_callback["callback_text"]
    try:
        movies_list = get_list_movies_by_budget(
            flag_min_or_max=flag, limit=int(curr_limit)
        )
        user_id_for_telegram = call.from_user.id
        user = User.get_or_none(User.telegram_id == user_id_for_telegram)

        if movies_list is not None:
            for i_movie in movies_list:
                movie = Movie(i_movie)
                bot.send_photo(call.from_user.id, movie.poster)
                bot.send_message(call.from_user.id, movie)

                add_movie_to_history_requests(user, movie)

            with bot.retrieve_data(
                user_id=call.from_user.id, chat_id=call.message.chat.id
            ) as info_by_callback:
                call_text = info_by_callback["callback_text"]

            bot.send_message(
                chat_id=call.from_user.id,
                text="Что делаем дальше?",
                reply_markup=keyboard_menu_or_reply(call_text),
            )
            bot.delete_state(
                call.from_user.id,
            )

        else:
            bot.send_message(call.from_user.id, "Возникла ошибка.")

    except NotFoundMovie as exc:
        bot.send_message(call.from_user.id, text=exc)
