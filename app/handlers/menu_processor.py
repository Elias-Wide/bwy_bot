"""Модуль главного и других меню."""

from aiogram.types import FSInputFile, InlineKeyboardMarkup, InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import STATIC_DIR
from app.core.constants import (
    DIET,
    FMT_JPG,
    INTRO_SETTINGS_TEXT,
    OOPS_DIET,
    SETTINGS,
    SleepMode,
)
from app.core.logging import get_logger
from app.exceptions.workout import NoExerciseException
from app.handlers.callbacks import (
    calorie_counter,
    select_workout,
    workout_exercises,
    workouts_by_group,
)
from app.handlers.sleep_handlers import (
    go_to_bed_menu,
    sleep_duration_menu,
    sleep_mode_menu,
    sleep_statistic_menu,
    wake_up_menu,
)
from app.keyboards import get_main_menu_btns, get_oops_kb, get_settings_btns
from app.models import User
from app.utils.utils import get_banner, get_reminder_state

logger = get_logger(__name__)


async def main_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Возвращает главное меню."""
    return (
        await get_banner(menu_name, level),
        get_main_menu_btns(level=level),
    )


async def settings_menu(
    level: int,
    menu_name: str,
    user: User,
    session: AsyncSession,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Получить состояние переключателей и вывести."""
    res = await get_reminder_state(user, session)
    try:
        image = FSInputFile(STATIC_DIR.joinpath(menu_name + FMT_JPG))
    except NoExerciseException:
        return (
            await get_banner(OOPS_DIET, level),
            get_oops_kb(level=level, menu_name=menu_name),
        )
    return (
        InputMediaPhoto(
            media=image,
            caption=(f'{INTRO_SETTINGS_TEXT}\n' f'{res}'),
        ),
        get_settings_btns(level=level),
    )


async def get_menu_content(
    level: int,
    menu_name: str,
    user: User,
    session: AsyncSession | None = None,
    workout_group: str | None = None,
    workout_id: int | None = None,
    page: int | None = None,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Возвращает контент в зависимости от level и menu_name."""
    match level:
        case 0:
            if menu_name == DIET:
                return await calorie_counter(level, menu_name, user, session)
            if menu_name == SETTINGS:
                return await settings_menu(level, menu_name, user, session)
            return await main_menu(level, menu_name)
        case 1:
            if menu_name == SleepMode.SLEEP:
                return await sleep_mode_menu(level, menu_name)
            return await select_workout(
                session,
                level,
                menu_name,
            )
        case 2:
            if menu_name == SleepMode.GO_TO_BED:
                return await go_to_bed_menu(level, menu_name, user, session)
            if menu_name == SleepMode.WAKE_UP:
                return await wake_up_menu(level, menu_name, user, session)
            if menu_name == SleepMode.DURATION:
                return await sleep_duration_menu(level, menu_name)
            if menu_name == SleepMode.STATISTIC:
                return await sleep_statistic_menu(
                    level,
                    menu_name,
                    user,
                    session,
                )
            return await workouts_by_group(
                session,
                user,
                level,
                menu_name,
                workout_group,
            )
        case _:
            return await workout_exercises(
                session=session,
                level=level,
                user=user,
                menu_name=menu_name,
                workout_id=workout_id,
                workout_group=workout_group,
                page=page,
            )
