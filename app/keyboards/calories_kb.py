from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.constants import BACK, MAIN_MENU, DEFAULT_KEYBOARD_SIZE
from app.keyboards.mode_kb import MenuCallBack


def get_calories_btns(
    *,
    level: int,
    sizes: tuple[int] = DEFAULT_KEYBOARD_SIZE,
) -> InlineKeyboardMarkup:
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
