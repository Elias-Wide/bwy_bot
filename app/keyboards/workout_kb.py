from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.constants import (
    ACTIVITY_KEYBOARD_SIZE,
    BACK,
    BACKWARD,
    COMPLETE,
    DEFAULT_KEYBOARD_SIZE,
    FORWARD,
    MAIN_MENU,
    WORKOUTS,
)
from app.keyboards.mode_kb import MenuCallBack
from app.models import Workout


def get_workout_select_btns(
    *,
    level: int,
    groups: list[Workout],
    sizes: tuple[int] = DEFAULT_KEYBOARD_SIZE,
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=BACK,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=MAIN_MENU,
            ).pack(),
        ),
    )
    for group in groups:
        keyboard.add(
            InlineKeyboardButton(
                text=group.group.value,
                callback_data=MenuCallBack(
                    level=level + 1,
                    menu_name=group.group.code,
                    workout_group=group.id,
                ).pack(),
            ),
        )
    return keyboard.adjust(*sizes).as_markup()


def get_exercise_btns(
    *,
    level: int,
    menu_name: str,
    workout_group: int,
    page: int,
    pagination_btns: dict,
    sizes: tuple[int] = ACTIVITY_KEYBOARD_SIZE,
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=COMPLETE,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=WORKOUTS,
            ).pack(),
        ),
    )
    keyboard.adjust(*sizes)

    row = []
    for text, menu_name in pagination_btns.items():
        if menu_name == FORWARD:
            row.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                        workout_group=workout_group,
                        page=page + 1,
                    ).pack(),
                ),
            )
        elif menu_name == BACKWARD:
            row.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                        workout_group=workout_group,
                        page=page - 1,
                    ).pack(),
                ),
            )

    return keyboard.row(*row).as_markup()
