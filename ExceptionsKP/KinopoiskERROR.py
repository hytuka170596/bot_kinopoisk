from typing import TypeAlias
from model.UserForKinopoisk import User

MessageError: TypeAlias = str


class RequestErrorLimit(Exception):
    def __init__(self):
        self.message: MessageError = "К сожалению превышен лимит запросов в 200 шт. в день"
        super().__init__(self.message)


class NotFoundMovie(Exception):
    def __init__(self):
        self.message: MessageError = "Такого фильма нет на сайте, либо неверно указано название"
        super().__init__(self.message)


class ErrorCurrentYearKP(ValueError):
    def __init__(self):
        self.message: MessageError = "Указан некорректный год, измените данные."
        super().__init__(self.message)


class InputErrorDateKP(ValueError):
    def __init__(self, date: str):
        self.date = date
        self.message: MessageError = ("Указан неверный формат - {error_format}\n Напишите дату в формате (ДД.ММ.ГГГГ):".
                                      format(error_format=self.date))
        super().__init__(self.message)


class HistoryNotFoundError(AttributeError):
    def __init__(self, date):
        self.date = date
        self.message: MessageError = (f"История запросов пуста за указанную дату {self.date}. "
                                      f"\nВы ещё ничего не искали в этот день.")
        super().__init__(self.message)


class NotHistoryRequest(AttributeError):
    def __init__(self, user: User):
        self.user = user.username
        self.message: MessageError = "{name} - ваша история запросов пуста".format(name=self.user)
        super().__init__(self.message)
