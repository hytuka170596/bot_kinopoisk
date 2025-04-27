from telebot.types import Message
from loader import bot
from model.UserForKinopoisk import User
from peewee import IntegrityError
from keyboards.inline.Kinopoisk_Keyboard import menu_main


@bot.message_handler(commands=["start"])
def handle_start(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    try:
        User.create(
            telegram_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        bot.reply_to(
            message,
            "Добро пожаловать в менеджер задач!🫡\n"
            "Вы тут впервые, для начала советую написать команду /help,"
            "чтобы получить информацию о боте!",
        )
    except IntegrityError:
        bot.send_message(
            user_id,
            "Выберете способ поиска из предложенных ниже👇\n",
            reply_markup=menu_main(),
        )
