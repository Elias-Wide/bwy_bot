from typing import Iterable

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.core.logging import get_logger

logger = get_logger(__name__)

from app.core.constants import DEFAULT_KEYBOARD_SIZE



async def create_survey_kb(
    items: Iterable[str],
    callback_datas: Iterable[str | None] = (None,),
    size: tuple[int] = DEFAULT_KEYBOARD_SIZE,
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item, callback_data in zip(items, callback_datas):
        builder.add(
            InlineKeyboardButton(text=item, callback_data=callback_data),
        )
        logger.info(f'{item}  -- {callback_data}')
    return builder.adjust(*size).as_markup()
