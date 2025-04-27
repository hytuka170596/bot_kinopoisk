from telebot.handler_backends import State, StatesGroup


class MovieStateInfo(StatesGroup):
    get_name_movie = State()
    get_limit_movies = State()
    get_movies_by_rating = State()
    get_year_for_user = State()
    get_limit_movie = State()
    get_movies_by_budget = State()
    get_value_limit = State()
    get_movie_count = State()
    get_movie_count_1 = State()
    added_genre = State()


class HistoryState(StatesGroup):

    get_date = State()
    get_limit = State()
    get_film = State()
