from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DIET, SleepMode
from app.core.logging import get_logger
from app.handlers.callbacks import calorie_counter, select_workout, workouts
from app.keyboards import (
    get_main_menu_btns,
    get_sleep_back_btns,
    get_sleep_back_btns_duration,
    get_sleep_select_btns,
)
from app.models.user import User
from app.utils.utils import get_banner

logger = get_logger(__name__)


async def main_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    return (
        await get_banner(menu_name, level),
        get_main_menu_btns(level=level),
    )


async def sleep_mode_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    return (
        await get_banner(menu_name, level),
        get_sleep_select_btns(level=level),
    )


async def go_to_bed_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Ответ времени отхода ко сну."""
    return (
        await get_banner(menu_name, level),
        get_sleep_back_btns(level=level),
    )


async def wake_up_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Ответ времени пробуждения."""
    return (
        await get_banner(menu_name, level),
        get_sleep_back_btns(level=level),
    )


async def sleep_duration_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Ввод продолжительности сна."""
    return (
        await get_banner(menu_name, level),
        get_sleep_back_btns_duration(level=level),
    )


async def sleep_statistic_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Ввод продолжительности сна."""
    return (
        await get_banner(menu_name, level),
        get_sleep_back_btns(level=level),
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
            if menu_name == SleepMode.SLEEP:
                return await sleep_mode_menu(level, menu_name)
            return await select_workout(
                session,
                user,
                level,
                menu_name,
            )
        case 2:
            if menu_name == SleepMode.GO_TO_BED:
                return await go_to_bed_menu(level, menu_name)
            if menu_name == SleepMode.WAKE_UP:
                return await wake_up_menu(level, menu_name)
            if menu_name == SleepMode.DURATION:
                return await sleep_duration_menu(level, menu_name)
            if menu_name == SleepMode.STATISTIC:
                return await sleep_statistic_menu(level, menu_name)
            return await workouts(
                session,
                level,
                menu_name,
                workout_group,
                page,
            )
