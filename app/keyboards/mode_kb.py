from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.lexicon.lexicon import LEXICON


async def create_mode_kb() -> ReplyKeyboardBuilder:
    kb_builder = ReplyKeyboardBuilder()
    mode_buttons: list[KeyboardButton] = [
        KeyboardButton(text=mode) for mode in LEXICON['mode'].values()
    ]
    kb_builder.row(*mode_buttons, width=1)
    return kb_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)
