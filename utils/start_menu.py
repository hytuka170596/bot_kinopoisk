from config_data.config import DEFAULT_COMMANDS
from telebot.types import BotCommand


def start_menu(bot):
    """Функция устанавливает в панели телеграмм меню рабочие команды текущего бота."""
    bot.set_my_commands([BotCommand(*command) for command in DEFAULT_COMMANDS])
