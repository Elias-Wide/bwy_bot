from typing import TypeAlias

from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


BUTTONS = {'Сон💤': 'sleep', 'Питание🥦': 'diet', 'Тренировки🏋‍♂️': 'workouts'}


class MenuCallBack(CallbackData, prefix='menu'):
    """
    Фабрика колбэков.

    level :: атрибут указывающий на глубину(шаг) меню. Пример:
     Главное_меню(0) -> Тренировки(1) -> Кардио(2)

    menu_name :: название меню.
    """

    level: int
    menu_name: str


def get_main_menu_btns(
    *,
    level: int,
    sizes: tuple[int] = (2,),
) -> KeyboardMarkup:
    """Генератор клавиатуры главного меню."""
    keyboard = InlineKeyboardBuilder()

    for text, menu_name in BUTTONS.items():
        if menu_name == 'workouts':
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
