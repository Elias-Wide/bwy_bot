from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenuCallBack(CallbackData, prefix='menu'):
    """
    Фабрика колбэков.

    level :: атрибут указывающий на глубину(шаг) меню. Пример:
     Главное_меню(0) -> Тренировки(1) -> Кардио(2)

    menu_name :: название меню.
    """

    level: int
    menu_name: str


def get_main_menu_btns(
    *, level: int, sizes: tuple[int] = (2,)
) -> InlineKeyboardMarkup:
    """Генератор клавиатуры главного меню."""
    keyboard = InlineKeyboardBuilder()
    buttons = {
        'Сон💤': 'sleep',
        'Питание🥦': 'diet',
        'Тренировки🏋‍♂️': 'workout'
    }
    for text, menu_name in buttons.items():
        keyboard.add(InlineKeyboardButton(
            text=text,
            callback_data=MenuCallBack(
                level=level + 1,
                menu_name=menu_name
            ).pack()
        ))

    return keyboard.adjust(*sizes).as_markup()
