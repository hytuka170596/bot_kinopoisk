from loader import bot
from telebot.types import Message


@bot.message_handler(commands=["help"])
def start(message: Message):
    bot.send_message(
        message.from_user.id,
        'Это бот поиска фильмов\сериалов по сайту "Кинопоиск"\n'
        "Он умеет искать фильмы по названию, рейтингу, бюджету, и по годам.\n"
        "А так же сохраняет историю запросов.",
    )
