from typing import Iterable

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def create_survey_kb(items: Iterable[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=item) for item in items]],
        resize_keyboard=True,
    )
