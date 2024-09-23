"""Модуль клавиатуры для напоминаний."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.core.constants import (
    DIET,
    KB_TEXT_FOR_DIET,
    KB_TEXT_FOR_SLEEPING,
    KB_TEXT_FOR_TRAINING,
    SLEEP,
    WORKOUTS,
)


def get_remind_button(
    remind_type: str,
) -> InlineKeyboardMarkup:
    """Получить кнопку для соответствующего напоминания."""
    if remind_type == DIET:
        text, callback_data = KB_TEXT_FOR_DIET, DIET
    elif remind_type == WORKOUTS:
        text, callback_data = KB_TEXT_FOR_TRAINING, WORKOUTS
    elif remind_type == SLEEP:
        text, callback_data = KB_TEXT_FOR_SLEEPING, SLEEP
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=callback_data)],
        ],
    )
