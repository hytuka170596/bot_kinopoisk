from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot_pagination import InlineKeyboardPaginator
from loader import bot
from model.UserForKinopoisk import Movie


def menu_main() -> InlineKeyboardMarkup:
    """Клавиатура главного меню"""
    keyboard = InlineKeyboardMarkup(row_width=2)

    button_1 = InlineKeyboardButton(
        text="🎞 Поиск по названию 🎞", callback_data="movie_search"
    )
    button_2 = InlineKeyboardButton(text="📉 По рейтингу 📉", callback_data="rating")
    button_3 = InlineKeyboardButton(
        text="🤓 С низким бюджетом 😢", callback_data="low_budget_movie"
    )
    button_4 = InlineKeyboardButton(
        text="👆 С высоким бюджетом 👍", callback_data="high_budget_movie"
    )
    button_5 = InlineKeyboardButton(text="🕑 По годам 🕖", callback_data="year")
    button_6 = InlineKeyboardButton(
        text="💾 История запросов 💾", callback_data="history"
    )
    keyboard.add(button_1, button_2, button_3, button_4, button_5, button_6)

    return keyboard


def keyboard_menu_or_reply(callback_text: str) -> InlineKeyboardMarkup:

    buttons_for_reply = {
        "movie_search": "🎞 Поиск по названию 🎞",
        "rating": "📉 По рейтингу 📉",
        "year": "🕑 По годам 🕖",
        "low_budget_movie": "🤓 С низким бюджетом 😢",
        "high_budget_movie": "👆 С высоким бюджетом 👍",
        "history": "💾 История запросов 💾"
    }
    text_button = buttons_for_reply[callback_text]
    keyboard = InlineKeyboardMarkup(row_width=3)

    button_1 = InlineKeyboardButton(text=text_button, callback_data=callback_text)
    button_2 = InlineKeyboardButton(
        text="Вернуться в основное меню ⬅️", callback_data="main_menu"
    )
    keyboard.add(button_1)
    keyboard.add(button_2)

    return keyboard


def keyboard_with_ratings() -> InlineKeyboardMarkup:
    """
    Клавиатура выбора рейтинга пользователем
    """
    list_rating = [
        "5",
        "5 - 6",
        "5 - 7",
        "5 - 8",
        "5 - 9",
        "5 - 10",
        "6",
        "6 - 7",
        "6 - 8",
        "6 - 9",
        "6 - 10",
        "7",
        "7 - 8",
        "7 - 9",
        "7 - 10",
        "8",
        "8 - 9",
        "8 - 10",
        "9",
        "9 - 10",
        "10",
    ]

    keyboard = InlineKeyboardMarkup(row_width=7)
    buttons = [
        InlineKeyboardButton(text=rating, callback_data=rating)
        for rating in list_rating
    ]
    keyboard.add(*buttons)

    return keyboard


def keyboard_with_years() -> InlineKeyboardMarkup:
    """Клавиатура для выбора периода поиска кино"""
    keyboard = InlineKeyboardMarkup(row_width=7)

    buttons = [
        InlineKeyboardButton(text=year, callback_data=f"{str(year)}-year")
        for year in range(1980, 2025)
    ]
    keyboard.add(*buttons)

    return keyboard


def keyboard_with_get_value_limit() -> InlineKeyboardMarkup:
    """Клавиатура для выбора лимита выводимых фильмов под запрос"""
    keyboard = InlineKeyboardMarkup(row_width=5)

    buttons = [
        InlineKeyboardButton(text=digit, callback_data=digit) for digit in range(1, 16)
    ]
    keyboard.add(*buttons)

    return keyboard


def keyboard_by_genre() -> InlineKeyboardMarkup:
    """Клавиатура для выбора жанра"""
    genres = {
        "Аниме": "anime",
        "Комедия": "comedy",
        "Драма": "drama",
        "Боевик": "action",
        "Фантастика": "sci-fi",
        "Ужасы": "horror",
        "Триллер": "thriller",
        "Мелодрама": "romance",
        "Фэнтези": "fantasy",
        "Приключения": "adventure",
        "Мультфильм": "animation",
        "Документальный": "documentary",
        "Криминал": "crime",
        "Вестерн": "western",
        "Исторический": "historical",
        "Музыкальный": "musical",
        "Биография": "biography",
        "Семейный": "family",
        "Спортивный": "sports",
        "Военный": "military",
    }

    keyboard = InlineKeyboardMarkup(row_width=4)
    buttons = [
        InlineKeyboardButton(text=genre, callback_data=genres[genre])
        for genre in genres
    ]
    button = InlineKeyboardButton(text="Показать подборку", callback_data='stop')
    keyboard.add(*buttons)
    keyboard.add(button)

    return keyboard


def menu_history(history_requests: list, current_page: int = 0) -> tuple:
    """ Клавиатура для просмотра фильмов из истории запросов. """

    paginator = InlineKeyboardPaginator(
        page_count=len(history_requests),
        current_page=current_page,
        data_pattern='history_{page}'
    )

    paginator.add_before(
        InlineKeyboardButton(text="<<", callback_data='back_to_end'),
        InlineKeyboardButton(text="<", callback_data='back'),
        InlineKeyboardButton(text="-{}-".format(current_page+1), callback_data='current'),
        InlineKeyboardButton(text=">", callback_data='next'),
        InlineKeyboardButton(text=">>", callback_data='next_to_end')
    )

    return paginator.markup
