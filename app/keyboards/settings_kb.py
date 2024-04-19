from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards.mode_kb import MenuCallBack

BUTTONS = {
    'Тренировки': 'stop_train',
    'Сон': 'stop_sleep',
    'Калории': 'stop_calorie',
}


def get_settings_btns(
    *,
    level: int,
    sizes: tuple[int] = (2,),
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for text, menu_name in BUTTONS.items():
        keyboard.add(
            InlineKeyboardButton(
                text=text,
                callback_data=menu_name,
                )
        )
    keyboard.add(
        InlineKeyboardButton(
            text='Назад👈',
            callback_data=MenuCallBack(
                level=level,
                menu_name='main',
            ).pack(),
        ),
    )
    return keyboard.adjust(*sizes).as_markup()