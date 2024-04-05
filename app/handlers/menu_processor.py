import os
from aiogram.types import FSInputFile, InputMediaPhoto

from core.config import settings
from keyboards import get_main_menu_btns


async def main_menu(level, menu_name):
    """
    Функция генерирующая главное меню.

    Загружает лого из каталога со статикой, добавляет к нему описание и
     возвращает в хэндлер для отправки пользователю.
    """
    banner_path = os.path.join(
        str(settings.base_dir), 'static', menu_name + '.jpg'
    )
    banner = FSInputFile(banner_path)
    description = ('Добро пожаловать в Ваш личный помощник'
                   ' самосовершенствования.')
    image = InputMediaPhoto(media=banner, caption=description)
    keyboard = get_main_menu_btns(level=level)
    return image, keyboard


async def get_menu_content(level: int, menu_name: str):
    """Диспетчер меню."""
    if level == 0:
        return await main_menu(level, menu_name)
