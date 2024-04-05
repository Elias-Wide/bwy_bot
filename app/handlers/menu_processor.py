from aiogram.types import FSInputFile, InlineKeyboardMarkup, InputMediaPhoto

from app.core.config import settings
from app.keyboards import get_main_menu_btns


async def main_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]
    """
    Функция генерирующая главное меню.

    Загружает лого из каталога со статикой, добавляет к нему описание и
     возвращает в хэндлер для отправки пользователю.
    """
    banner_path = settings.base_dir.joinpath('static', menu_name + '.jpg')
    image = InputMediaPhoto(
        media=FSInputFile(banner_path),
        caption='Добро пожаловать в Ваш личный помощник самосовершенствования.'
    )
    keyboard = get_main_menu_btns(level=level)
    return image, keyboard


async def get_menu_content(level: int, menu_name: str):    # TODO: сделать анотацию по завершении функции!
    """Диспетчер меню."""
    if level == 0:
        return await main_menu(level, menu_name)
