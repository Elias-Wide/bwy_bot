from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DIET, SleepMode
from app.core.logging import get_logger
from app.handlers.callbacks import calorie_counter, select_workout, workouts
from app.handlers.callbacks.sleep import (
    go_to_bed_menu,
    sleep_duration_menu,
    sleep_mode_menu,
    sleep_statistic_menu,
    wake_up_menu,
)
from app.keyboards import get_main_menu_btns, get_settings_btns
from app.models.user import User
from app.utils.utils import get_banner, get_reminder_state

logger = get_logger(__name__)


async def main_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
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
    res = await get_reminder_state(user, session)
    return (
        InputMediaPhoto(
            media=await get_banner(menu_name),
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
    session: AsyncSession | None = None,
    workout_group: int | None = None,
    page: int | None = None,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    match level:
        case 0:
            if menu_name == DIET:
                return await calorie_counter(level, menu_name, user, session)
            if menu_name == 'settings':
                return await settings_menu(level, menu_name, user, session)
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
