from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.logging import get_logger
from app.keyboards.mode_kb import MenuCallBack

logger = get_logger(__name__)

SLEEP_BUTTONS = {
        'Ложусь спать': 'go_to_bed',
        'Проснулся': 'wake_up',
        'Продолжительность сна': 'sleep_duration',
        'Статистика': 'sleep_statistic',
}


def get_sleep_select_btns(
    *,
    level: int,
    sizes: tuple[int] = (2,),
) -> InlineKeyboardMarkup:
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
            text='Назад👈',
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name='main',
            ).pack(),
        ),
    )
    return keyboard.adjust(*sizes).as_markup()


def get_sleep_back_btns(
    *,
    level: int,
    sizes: tuple[int] = (2,),
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text='ОК👍',
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name='sleep',
            ).pack(),
        ),
    )
    keyboard.add(
        InlineKeyboardButton(
            text='Назад👈',
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name='sleep',
            ).pack(),
        ),
    )
    return keyboard.adjust(*sizes).as_markup()


def get_sleep_back_btns_duration(
    *,
    level: int,
    sizes: tuple[int] = (2,),
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text='Да',
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name='sleep',
            ).pack(),
        ),
    )

    keyboard.add(
        InlineKeyboardButton(
            text='Нет👎',
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name='sleep',
            ).pack(),
        ),
    )
    keyboard.add(
        InlineKeyboardButton(
            text='Назад👈',
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name='sleep',
            ).pack(),
        ),
    )
    return keyboard.adjust(*sizes).as_markup()
