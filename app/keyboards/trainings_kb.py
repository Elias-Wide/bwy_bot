from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
    ReplyKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.lexicon.lexicon import LEXICON


async def create_select_training_kb() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    training_buttons: list[KeyboardButton] = [
        KeyboardButton(text=training)
        for training in LEXICON['workout'].values()
    ]
    kb_builder.row(*training_buttons, width=3)
    return kb_builder.as_markup(on_time_keyboard=True, resize_keyboard=True)


async def create_pagination_kb(*buttons: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON[button] if button in LEXICON else button,
        callback_data=button,
    ) for button in buttons
    ])
    return kb_builder.as_markup()
