from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.constants import (
    ACTIVITY_KEYBOARD_SIZE, BACK, BUTTONS_FOR_TRAINING,
    COMPLETE, DEFAULT_KEYBOARD_SIZE, MAIN_MENU, NEXT, WORKOUTS
)
from app.keyboards.mode_kb import MenuCallBack


def get_workout_select_btns(
    *,
    level: int,
    sizes: tuple[int] = DEFAULT_KEYBOARD_SIZE,
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for text, menu_name in BUTTONS_FOR_TRAINING['category'].items():
        keyboard.add(
            InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    level=level + 1,
                    menu_name=menu_name,
                ).pack(),
            ),
        )
    keyboard.add(
        InlineKeyboardButton(
            text=BACK,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=MAIN_MENU,
            ).pack(),
        ),
    )
    return keyboard.adjust(*sizes).as_markup()


def get_workout_bts(
    *,
    level: int,
    menu_name: str,
    sizes: tuple[int] = ACTIVITY_KEYBOARD_SIZE,
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text=NEXT,
            callback_data=MenuCallBack(
                level=level,
                menu_name=menu_name,
            ).pack(),
        ),
    )
    keyboard.add(
        InlineKeyboardButton(
            text=COMPLETE,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=WORKOUTS,
            ).pack(),
        ),
    )
    return keyboard.adjust(*sizes).as_markup()
