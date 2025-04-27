<h1 align="center">Здравствуйте!
Это телеграмм бот для поиска фильмов по сайту >>>
<a href="https://www.kinopoisk.ru/" target="_blank">Кинопоиск</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
<h2 align="center">Вся информация и документация по работе с API находится на этом сайте >>>
<a href="https://kinopoisk.dev/" target="_blank">Кинопоиск.dev</a> </h2>
<h3 align="center">Чтобы получить ТОКЕН для своего телеграмм бота, 
напишите боту в телеграмме >>>
<a href="https://t.me/BotFather" target="_blank">BotFather</a> </h3>
<h1 align="center">Подробная информация 👇 </h1>



    Для чего создан этот проект:  
    
        Практическая работа по созданию телеграмм бота. 
        Развитие индивидуальных навыков!
        Получение опыта создания продукта на основе собственных знаний.
        Научиться основам работы с ORM и базами данных.
        Создание первой работы для портфолио.
    


Краткое описание как работать с ботом:


1. **Запуск бота**:
   - Напишите команду `/start` боту в Telegram, чтобы начать работу.

2. **Главное меню**:
   - Используйте главное меню для поиска фильмов по различным критериям, таким как название, рейтинг, бюджет, год и история запросов.

3. **Поиск по названию**:
   - Выберите опцию `🎞 Поиск по названию 🎞` и введите название фильма.

4. **Поиск по рейтингу**:
   - Выберите опцию `📉 По рейтингу 📉` и выберите интересующий вас диапазон рейтингов.

5. **Поиск по бюджету**:
   - Выберите опцию `🤓 С низким бюджетом 😢` или `👆 С высоким бюджетом 👍` для поиска фильмов по бюджету.

6. **Поиск по годам**:
   - Выберите опцию `🕑 По годам 🕖` и выберите интересующий вас год.

7. **История запросов**:
   - Выберите опцию `💾 История запросов 💾` для просмотра ранее искомых фильмов.

## Установка и настройка

1. **Клонирование репозитория**:
   ```bash
   git clone https://github.com/hytuka170596/bot_kinopoisk.git
   cd ваш репозиторий

    Установка зависимостей:

    pip install -r requirements.txt

    Настройка окружения:
        Создайте файл .env в корневой папке проекта и добавьте следующие переменные:

        BOT_TOKEN="Ваш токен для бота, полученный от @BotFather"
        TOKEN_KINOPOISK="Токен для kinopoiskdev" # нужно получить от телеграмм бота https://t.me/kinopoiskdev_bot
        API_KINOPOISK_BY_NAME="Метод поиска по имени из документации kinopoiskdev" # "https://api.kinopoisk.dev/v1.4/movie/search"
        API_KINOPOISK_BY_FILTER="Метод поиска по фильтрам из документации kinopoiskdev" # "https://api.kinopoisk.dev/v1.4/movie"


    Запуск бота:

    python main.py

Структура проекта
    

    main.py: Основной файл для запуска бота.
    loader.py: Инициализация бота и загрузка основных модулей.
    database/: Папка для хранения различных баз данных.
    ExceptionsKP/: Папка с исключениями для разных ошибок при работе с ботом.
    keyboards/: Папка с файлами клавиатур для различных меню.
    handlers/: Папка с обработчиками различных команд и сообщений.
    model/: Папка с моделями ORM для работы с базой данных.
    utils/: Папка с утилитами и вспомогательными функциями.
    state/: Папка с состояниями в которых мы будем ловить пользователя.
    .gitignore: Файл для указания файлов и папок, которые не должны быть добавлены в систему контроля версий Git.
    .env: Файл для хранения конфиденциальной информации, такой как API ключи, пароли и другие переменные среды.


Используемые технологии


    Python: Основной язык программирования.
    PyTelegramBotAPI: Библиотека для работы с Telegram Bot API.
    Peewee: ORM для работы с базой данных.
    SQLite: База данных для хранения информации о пользователях и их запросах.
    # рекомендуется использовать loguru для логирования, это более удобно и практично

Примеры кода:

(Основная логика работы вывода истории фильмов, которые были найдены ранее)


    from model.UserForKinopoisk import User
    from telebot.types import CallbackQuery
    from loader import bot
    from keyboards.inline.Kinopoisk_Keyboard import menu_main


        @bot.message_handler(commands=["history"])
        @bot.callback_query_handler(func=lambda call: call.data == "history")
        def get_history_for_user(message_or_call):
            if isinstance(message_or_call, CallbackQuery):
                user_id_for_telegram = message_or_call.from_user.id
                bot.edit_message_reply_markup(
                    chat_id=user_id_for_telegram, message_id=message_or_call.message.message_id
                )
            else:
                user_id_for_telegram = message_or_call.from_user.id
    
        user = User.get_or_none(User.telegram_id == user_id_for_telegram)
        if user is None:
            bot.send_message(
                user_id_for_telegram, "Вы не зарегистрированы. Напишите /start"
            )
            return
    
        history_requests = user.history_requests
        if not history_requests:
            bot.send_message(
                user_id_for_telegram, "История запросов пуста. Вы ещё ничего не искали."
            )
            bot.send_message(
                chat_id=user_id_for_telegram,
                text="Выберете способ поиска из предложенных ниже👇\n",
                reply_markup=menu_main(),
            )
    
        for request in history_requests:
            bot.send_photo(user_id_for_telegram, request.poster)
            bot.send_message(user_id_for_telegram, request)

Главное меню

    from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
    
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

