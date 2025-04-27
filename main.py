from loader import bot
from utils.start_menu import start_menu
from telebot.custom_filters import StateFilter
from model.UserForKinopoisk import create_model
import handlers


if __name__ == "__main__":
    create_model()
    bot.add_custom_filter(StateFilter(bot))
    start_menu(bot)
    bot.infinity_polling()
