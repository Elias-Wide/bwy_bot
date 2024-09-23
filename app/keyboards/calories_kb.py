"""Клавиатура контроля калорий."""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.constants import BACK, DEFAULT_KEYBOARD_SIZE, MAIN_MENU
from app.keyboards.mode_kb import MenuCallBack


def get_calories_btns(
    *,
    level: int,
    sizes: tuple[int] = DEFAULT_KEYBOARD_SIZE,
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    """Получить кнопку назад в меню контроля калорий."""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=BACK,
            callback_data=MenuCallBack(
                level=level,
                menu_name=MAIN_MENU,
            ).pack(),
        ),
    )
    return keyboard.adjust(*sizes).as_markup()
