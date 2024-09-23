"""Модуль утилит для пагинации."""

from math import ceil
from typing import Literal


class Paginator:
    """Класс пагинатора."""

    def __init__(self, array: list, page: int = 1, per_page: int = 1) -> None:
        """Инициализация экземпляра класса."""
        self.array = array
        self.per_page = per_page
        self.page = page
        self.len = len(self.array)
        self.pages = ceil(self.len / self.per_page)

    def __get_slice(self) -> list:
        """Получить срез."""
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page
        return self.array[start:stop]

    def get_page(self) -> list:
        """Получить страницу."""
        page_items = self.__get_slice()
        return page_items

    def has_forward(self) -> int | Literal[False]:
        """Проверить, есть ли следующая страница."""
        if self.page < self.pages:
            return self.page + 1
        return False

    def has_backward(self) -> int | Literal[False]:
        """Проверить, есть ли предыдущая страница."""
        if self.page > 1:
            return self.page - 1
        return False

    def get_next(self) -> list:
        """Получить следующую страницу."""
        if self.page < self.pages:
            self.page += 1
            return self.get_page()
        raise IndexError(
            'Next page does not exist. Use has_next() to check before.',
        )

    def get_previous(self) -> list:
        """Получить предыдущую страницу."""
        if self.page > 1:
            self.page -= 1
            return self.__get_slice()
        raise IndexError(
            'Previous page does not exist. Use has_previous() to check'
            ' before.',
        )


def get_pages(paginator: Paginator) -> dict:
    """Получить страницы."""
    buttons = {}

    if paginator.has_backward():
        buttons['⬅️ Пред.'] = 'backward'

    if paginator.has_forward():
        buttons['След. ➡️'] = 'forward'

    return buttons
