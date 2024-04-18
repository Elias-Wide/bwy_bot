from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards.mode_kb import MenuCallBack

def get_oops_kb(
    *,
    level: int,
    menu_name: str,
    sizes: tuple[int] = (1,)
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text='Назад👈',
        callback_data=MenuCallBack(
            level=level-1,
            menu_name='main' if menu_name == 'workouts' else 'workouts',
        ).pack()
    ))
    return keyboard.adjust(*sizes).as_markup()
