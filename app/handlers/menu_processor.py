from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DIET
from app.core.logging import get_logger
from app.keyboards import (
    get_calories_btns,
    get_main_menu_btns,
)
from app.models.user import User
from app.utils.utils import (
    _get_banner,
    get_calorie_plot,
)
from app.handlers.callbacks.workout import workout_category_menu, workouts

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
        await _get_banner(menu_name),
        get_main_menu_btns(level=level),
    )


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


async def get_menu_content(
    session: AsyncSession,
    level: int,
    menu_name: str,
    user: User,
    workout_group: int | None = None,
    page: int | None = None,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Диспетчер меню."""
    match level:
        case 0:
            if menu_name == DIET:
                return await calorie_counter(level, user, session)
            return await main_menu(level, menu_name)
        case 1:
            return await workout_category_menu(
                session,
                user,
                level,
                menu_name,
            )
        case 2:
            return await workouts(
                session,
                level,
                menu_name,
                workout_group,
                page,
            )
