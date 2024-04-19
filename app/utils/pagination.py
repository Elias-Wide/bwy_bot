from math import ceil
from typing import Literal


class Paginator:

    def __init__(self, array: list, page: int = 1, per_page: int = 1) -> None:
        self.array = array
        self.per_page = per_page
        self.page = page
        self.len = len(self.array)
        self.pages = ceil(self.len / self.per_page)

    def __get_slice(self) -> list:
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page
        return self.array[start:stop]

    def get_page(self) -> list:
        page_items = self.__get_slice()
        return page_items

    def has_forward(self) -> int | Literal[False]:
        if self.page < self.pages:
            return self.page + 1
        return False

    def has_backward(self) -> int | Literal[False]:
        if self.page > 1:
            return self.page - 1
        return False

    def get_next(self) -> list:
        if self.page < self.pages:
            self.page += 1
            return self.get_page()
        raise IndexError(
            'Next page does not exist. Use has_next() to check before.',
        )

    def get_previous(self) -> list:
        if self.page > 1:
            self.page -= 1
            return self.__get_slice()
        raise IndexError(
            'Previous page does not exist. Use has_previous() to check'
            ' before.',
        )


def get_pages(paginator: Paginator) -> dict:
    buttons = {}

    if paginator.has_backward():
        buttons['⬅️ Пред.'] = 'backward'

    if paginator.has_forward():
        buttons['След. ➡️'] = 'forward'

    return buttons
