"""Клавиатура вступительной анкеты."""

from typing import Iterable

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.constants import DEFAULT_KEYBOARD_SIZE


async def create_survey_kb(
    items: Iterable[str],
    callback_datas: Iterable[str | None] = (None,),
    size: tuple[int] = DEFAULT_KEYBOARD_SIZE,
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    """Создать клавиутуру вступительной анкеты."""
    builder = InlineKeyboardBuilder()
    for item, callback_data in zip(items, callback_datas):
        builder.add(
            InlineKeyboardButton(text=item, callback_data=callback_data),
        )
    return builder.adjust(*size).as_markup()
