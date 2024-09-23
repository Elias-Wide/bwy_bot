"""Модуль общей клавиатуры."""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.constants import BACK, MAIN_MENU, WORKOUTS
from app.keyboards.mode_kb import MenuCallBack


def get_oops_kb(
    *,
    level: int,
    menu_name: str,
    sizes: tuple[int] = (1,),
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    """Получить клавиатуру при возникновении ошибки."""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=BACK,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=MAIN_MENU if menu_name == WORKOUTS else WORKOUTS,
            ).pack(),
        ),
    )
    return keyboard.adjust(*sizes).as_markup()
