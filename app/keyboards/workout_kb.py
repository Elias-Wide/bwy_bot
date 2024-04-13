from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards.mode_kb import MenuCallBack

BUTTONS = {
    'category': {
        'Грудь\\Бицепс': 'pectoral',
        'Спина\\Плечи\\Трицепс': 'back',
        'Ноги': 'legs',
        'Кардио🏃‍♂️': 'cardio',
    },
    'pagination': {'backward': '◀️', 'forward': '▶️'},
}


def get_workout_select_btns(
    *,
    level: int,
    sizes: tuple[int] = (2,),
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for text, menu_name in BUTTONS['category'].items():
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


def get_workout_bts(
    *,
    level: int,
    menu_name: str,
    sizes: tuple[int] = (1,),
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
         text='След. ➡️',
         callback_data=MenuCallBack(
              level=level,
              menu_name=menu_name 
         ).pack(),
    ))
    keyboard.add(
        InlineKeyboardButton(
            text='Завершить⛔️',
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name='workouts',
            ).pack(),
        ),
    )
    return keyboard.adjust(*sizes).as_markup()
