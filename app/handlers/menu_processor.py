from aiogram.types import (
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo,
)

from app.core.logging import get_logger
from app.keyboards import (
    get_main_menu_btns,
    get_workout_bts,
    get_workout_select_btns,
)
from app.utils.utils import _get_banner, _get_videos

logger = get_logger(__name__)


async def main_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """
    Генератор главного меню.
    Оборачивает FSInputfile в InputMediaPhoto, получает клавиатуру и
    возвращает в хэндлер.
    """
<<<<<<< HEAD
    return (
        InputMediaPhoto(
            media=await _get_banner(menu_name),
            caption='Добро пожаловать в личный помощник самосовершенствования.'
        ),
        get_main_menu_btns(level=level),
    )


async def workout_category_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Генератор меню выбора группы тренировки."""
    return (
        InputMediaPhoto(
            media=await _get_banner(menu_name),
            caption='Какой вид тренировки предпочитаете?',
        ),
        get_workout_select_btns(level=level),
=======
    banner_path = BASE_DIR.joinpath('static', menu_name + '.jpg')
    image = InputMediaPhoto(
        media=FSInputFile(banner_path),
        caption=(
            'Добро пожаловать в Ваш личный помощник самосовершенствования.'
        ),
>>>>>>> feature/add-table-fields-DB
    )


async def workout_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaVideo, InlineKeyboardMarkup]:
    contents = await _get_videos(menu_name)
    video = InputMediaVideo(
        media=contents[0],  # TODO: пагинация.
        caption='Какое-то упражнение: описание упражнения!',
    )
    keyboard = get_workout_bts(level=level)
    return video, keyboard


async def get_menu_content(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Диспетчер меню."""
    match level:
        case 0:
            return await main_menu(level, menu_name)
        case 1:
            return await workout_category_menu(level, menu_name)
        case 2:
            return await workout_menu(level, menu_name)
