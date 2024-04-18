from typing import TypeAlias

from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.constants import WORKOUTS, BUTTONS, DEFAULT_KEYBOARD_SIZE
KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


class MenuCallBack(CallbackData, prefix='menu'):
    """
    Фабрика колбэков.

    level :: атрибут указывающий на глубину(шаг) меню. Пример:
     Главное_меню(0) -> Тренировки(1) -> Кардио(2)

    menu_name :: название меню.
    """

    level: int
    menu_name: str
    workout_group: int | None = None
    page: int = 1


def get_main_menu_btns(
    *,
    level: int,
    sizes: tuple[int] = DEFAULT_KEYBOARD_SIZE,
) -> KeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for text, menu_name in BUTTONS.items():
        if menu_name == WORKOUTS:
            keyboard.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level=level + 1,
                        menu_name=menu_name,
                    ).pack(),
                ),
            )
        else:
            keyboard.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                    ).pack(),
                ),
            )

    return keyboard.adjust(*sizes).as_markup()
