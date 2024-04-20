from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DIET
from app.core.logging import get_logger
from app.handlers.callbacks import calorie_counter, select_workout, workouts
from app.keyboards import get_main_menu_btns
from app.models.user import User
from app.utils.utils import get_banner

logger = get_logger(__name__)


async def main_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    return (
        await get_banner(menu_name),
        get_main_menu_btns(level=level),
    )


async def get_menu_content(
    level: int,
    menu_name: str,
    user: User,
    session: AsyncSession | None = None,
    workout_group: int | None = None,
    page: int | None = None,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    match level:
        case 0:
            if menu_name == DIET:
                return await calorie_counter(level, menu_name, user, session)
            return await main_menu(level, menu_name)
        case 1:
            return await select_workout(
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
