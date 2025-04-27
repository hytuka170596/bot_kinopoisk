from loader import bot
from telebot.types import Message


__text = "Простите😓 Такой команды пока не существует.\nОбратитесь в меню /help, чтобы получить нужную информацию"


@bot.message_handler(content_types=["text"])
def handler_no_command_text(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id, text=__text)
