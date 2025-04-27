from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from model.UserForKinopoisk import User, Movie, HistoryRequest
from loader import bot
from state.movie_search import HistoryState
from keyboards.inline.Kinopoisk_Keyboard import menu_main, keyboard_with_get_value_limit, keyboard_menu_or_reply
from ExceptionsKP.KinopoiskERROR import NotHistoryRequest


def checkout_validate(value: str) -> bool:
    return value.isdigit() and int(value) >= 1


@bot.message_handler(commands=["history"])
@bot.callback_query_handler(func=lambda call: call.data == "history")
def get_date_request(message_or_call: CallbackQuery | Message) -> None:

    if isinstance(message_or_call, CallbackQuery):
        user_id_for_telegram = message_or_call.from_user.id
        bot.edit_message_reply_markup(chat_id=user_id_for_telegram, message_id=message_or_call.message.message_id)
    else:
        user_id_for_telegram = message_or_call.from_user.id

    user = User.get_or_none(User.telegram_id == user_id_for_telegram)
    if not user:
        bot.send_message(user_id_for_telegram, "Вы не зарегистрированы. Напишите /start")
        return

    bot.set_state(user_id=user_id_for_telegram, state=HistoryState.get_limit)
    bot.send_message(chat_id=user_id_for_telegram,
                     text="Выберете сколько последних запросов вывести: ",
                     reply_markup=keyboard_with_get_value_limit())


@bot.message_handler(state=HistoryState.get_limit)
@bot.callback_query_handler(func=lambda call: True, state=HistoryState.get_limit)
def handler_value_limit(message_or_call: CallbackQuery | Message) -> None:
    if isinstance(message_or_call, CallbackQuery):
        user_id = message_or_call.from_user.id
        limit_value = message_or_call.data
        curr_message_id = message_or_call.message.message_id
    else:
        user_id = message_or_call.from_user.id
        limit_value = message_or_call.text
        curr_message_id = message_or_call.message_id - 1

    bot.edit_message_reply_markup(chat_id=user_id, message_id=curr_message_id)
    bot.delete_message(chat_id=user_id, message_id=curr_message_id)
    bot.delete_message(chat_id=user_id, message_id=curr_message_id-1)

    user = User.get_or_none(User.telegram_id == user_id)

    if checkout_validate(value=limit_value):
        try:
            history_requests = [
                request for request in user.history_requests.limit(int(limit_value))]
            if not history_requests:
                raise NotHistoryRequest(user)

            for request in history_requests:
                request: Movie
                bot.send_photo(user_id, request.poster)
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(text="Просмотрен", callback_data=f"viewed_{request.id}"))
                bot.send_message(chat_id=user_id, text=request, reply_markup=markup)

            call_text = "history"
            bot.send_message(
                chat_id=message_or_call.from_user.id,
                text="Что делаем дальше?",
                reply_markup=keyboard_menu_or_reply(call_text),
            )

        except NotHistoryRequest as exc:
            bot.send_message(user_id, str(exc))

        finally:
            bot.delete_state(user_id=user_id)

    else:
        bot.send_message(user_id, "Выберете число кнопкой или напишите целое число для запроса.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("viewed_"))
def handler_viewed(call: CallbackQuery) -> None:
    movie_id = call.data.split('_')[1]

    movie = HistoryRequest.get(HistoryRequest.id == movie_id)
    movie.viewed = True
    movie.save()
    bot.answer_callback_query(call.id, "Фильм отмечен как просмотренный!")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
