"""Модуль клавиатуры для меню сна."""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.constants import (
    BACK,
    MAIN_MENU,
    NO_BTN,
    OK_BTN,
    SLEEP_BUTTONS,
    YES_BTN,
    SleepMode,
)
from app.core.logging import get_logger
from app.keyboards.mode_kb import MenuCallBack
from app.models import User

logger = get_logger(__name__)


def get_sleep_select_btns(
    *,
    level: int,
    sizes: tuple[int] = (2,),
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    """Получить баннер и кнопки меню сна."""
    keyboard = InlineKeyboardBuilder()
    for text, menu_name in SLEEP_BUTTONS.items():
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


def get_sleep_back_btns(
    *,
    level: int,
    sizes: tuple[int] = (2,),
    user: User,
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    """Получить кнопки в разделе 'Ложусь спать'.

    Создает клавиатуру с кнопкой подтверждения и кнопкой 'Назад'.
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=OK_BTN,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=SleepMode.SLEEP,
                user=user,
                ok=SleepMode.GO_SLEEP_OK_BTN,
            ).pack(),
        ),
    )
    keyboard.add(
        InlineKeyboardButton(
            text=BACK,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=SleepMode.SLEEP,
            ).pack(),
        ),
    )
    return keyboard.adjust(*sizes).as_markup()


def get_wake_up_btns(
    *,
    level: int,
    sizes: tuple[int] = (2,),
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    """Получить кнопки в разделе 'Проснулся'.

    Создает клавиатуру с кнопкой подтверждения и кнопкой 'Назад'.
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=OK_BTN,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=SleepMode.SLEEP,
                ok=SleepMode.WAKE_UP_OK_BTN,
            ).pack(),
        ),
    )
    keyboard.add(
        InlineKeyboardButton(
            text=BACK,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=SleepMode.SLEEP,
            ).pack(),
        ),
    )
    return keyboard.adjust(*sizes).as_markup()


def get_sleep_back_btns_duration(
    *,
    level: int,
    sizes: tuple[int] = (2,),
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    """Получить кнопки подтверждения записи сна.

    Вызывается в разделе 'Продолжительность сна'.
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=YES_BTN,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=SleepMode.SLEEP,
                ok=SleepMode.DURATION_BTN,
                yes_no='yes',
            ).pack(),
        ),
    )
    keyboard.add(
        InlineKeyboardButton(
            text=NO_BTN,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=SleepMode.SLEEP,
                ok=SleepMode.DURATION_BTN,
                yes_no='no',
            ).pack(),
        ),
    )
    keyboard.add(
        InlineKeyboardButton(
            text=BACK,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=SleepMode.SLEEP,
            ).pack(),
        ),
    )
    return keyboard.adjust(*sizes).as_markup()


def get_sleep_statistic_btns(
    *,
    level: int,
    sizes: tuple[int] = (2,),
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    """Получить кнопки в меню статистика сна."""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=BACK,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=SleepMode.SLEEP,
            ).pack(),
        ),
    )
    return keyboard.adjust(*sizes).as_markup()


async def get_sleep_exist_btns(
    *,
    level: int,
    sizes: tuple[int] = (2,),
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    """Получить баннер и кнопки меню сна.

    Вызывается в меню сна при попытке записать данные
    отхода ко сну | подьема, если соответствующая запись уже есть.
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=BACK,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=SleepMode.SLEEP,
            ).pack(),
        ),
    )
    return keyboard.adjust(*sizes).as_markup()
