from aiogram.types import (
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DIET
from app.core.logging import get_logger
from app.keyboards import (
    get_calories_btns,
    get_main_menu_btns,
    get_settings_btns,
    get_workout_bts,
    get_workout_select_btns,
)
from app.models import User
from app.utils.utils import (
    _get_banner,
    _get_videos,
    calculation_of_calories,
    get_calorie_plot,
    get_reminder_state,
)

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
    return (
        InputMediaPhoto(
            media=await _get_banner(menu_name),
            caption='Добро пожаловать в Ваш личный помощник'
            ' самосовершенствования.',
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
    )


async def workout_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaVideo, InlineKeyboardMarkup]:
    content = await _get_videos()
    video = InputMediaVideo(
        media=content[0],
        caption='Какое-то упражнение: описание упражнения!',
    )
    keyboard = get_workout_bts(level=level, menu_name=menu_name)
    return video, keyboard


async def calorie_counter(
    level: int,
    user: User,
    session: AsyncSession,
) -> tuple[InputMediaPhoto]:
    """Ответ по каллоражу на день."""
    res = await calculation_of_calories(user)
    return (
        InputMediaPhoto(
            media=await get_calorie_plot(user, session),
            caption=f'Ваша норма калорий на день {res} Ккал',
        ),
        get_calories_btns(level=level),
    )


async def settings_menu(
    level: int,
    menu_name: str,
    user: User,
    session: AsyncSession,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Получить состояние переключателей и вывести."""
    res = await get_reminder_state(user, session)
    return (
        InputMediaPhoto(
            media=await _get_banner(menu_name),
            caption=(
                'Здесь вы можете управлять напоминаними. '
                'Нажатие на соответствующую кнопку включит '
                'или отключит напоминание. Отключение напоминания о '
                'тренировках отключает очередность упражнений расчитанных '
                'программой для Вас. '
                'Вы сможете сами выбирать их в ручную в соответствии с Вашими '
                'предпочтениями.'
                f'\n {res}'
            ),
        ),
        get_settings_btns(level=level),
    )


async def get_menu_content(
    level: int,
    menu_name: str,
    user: User,
    session: AsyncSession,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Диспетчер меню."""
    match level:
        case 0:
            if menu_name == 'settings':
                return await settings_menu(level, menu_name, user, session)
            if menu_name == DIET:
                return await calorie_counter(level, user, session)
            return await main_menu(level, menu_name)
        case 1:
            return await workout_category_menu(level, menu_name)
        case 2:
            return await workout_menu(level, menu_name)
