"""Клавиатура меню тренировок."""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.constants import (
    ACTIVITY_KEYBOARD_SIZE,
    BACK,
    BACKWARD,
    COMPLETE,
    DEFAULT_KEYBOARD_SIZE,
    FORWARD,
    MAIN_MENU,
    RANDOM_WORKOUT,
    TRAIN,
    WORKOUT_TYPE,
    WORKOUTS,
)
from app.core.logging import get_logger
from app.keyboards.mode_kb import MenuCallBack
from app.models import Workout

logger = get_logger(__name__)


def get_workout_select_btns(
    *,
    level: int,
    sizes: tuple[int] = DEFAULT_KEYBOARD_SIZE,
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    """Получить баннер и кнопки выбора типа тренировки.

    Выбор из групп тренировок, прописанных в константах.
    """
    keyboard = InlineKeyboardBuilder()
    for code, value in WORKOUT_TYPE:
        keyboard.add(
            InlineKeyboardButton(
                text=value,
                callback_data=MenuCallBack(
                    level=level + 1,
                    menu_name=TRAIN,
                    workout_group=code,
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


def get_workout_btns(
    *,
    level: int,
    workouts: list[Workout],
    workout_group: str,
    sizes: tuple[int] = DEFAULT_KEYBOARD_SIZE,
) -> InlineKeyboardMarkup:
    """Получить баннер и кнопки тренировок.

    Передается список тенировок выбранной группы, в соответствии с ним
    создаются кнопки с названиями тренировок.
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=RANDOM_WORKOUT,
            callback_data=MenuCallBack(
                level=level + 1,
                menu_name=TRAIN,
                workout_group=workout_group,
                workout_id=None,
            ).pack(),
        ),
    )
    for workout in workouts:
        keyboard.add(
            InlineKeyboardButton(
                text=workout.name,
                callback_data=MenuCallBack(
                    level=level + 1,
                    menu_name=TRAIN,
                    workout_group=workout_group,
                    workout_id=workout.id,
                ).pack(),
            ),
        )
    keyboard.add(
        InlineKeyboardButton(
            text=BACK,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=WORKOUTS,
            ).pack(),
        ),
    )
    return keyboard.adjust(*sizes).as_markup()


def get_exercise_btns(
    *,
    level: int,
    menu_name: str,
    workout_id: int,
    page: int,
    pagination_btns: dict,
    workout_group: str,
    sizes: tuple[int] = ACTIVITY_KEYBOARD_SIZE,
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    """Получить кнопки переключения между упражнениями."""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=COMPLETE,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=TRAIN,
                workout_group=workout_group,
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
                        workout_id=workout_id,
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
                        workout_id=workout_id,
                        workout_group=workout_group,
                        page=page - 1,
                    ).pack(),
                ),
            )

    return keyboard.row(*row).as_markup()
