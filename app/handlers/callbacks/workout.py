from aiogram.types import (
    FSInputFile,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import OOPS
from app.core.logging import get_logger
from app.crud import workout_crud
from app.exceptions.workout import NoExerciseException, NoWorkoutsException
from app.keyboards import (
    get_exercise_btns,
    get_oops_kb,
    get_workout_select_btns,
)
from app.models import User
from app.utils.pagination import Paginator, get_pages
from app.utils.utils import get_banner

logger = get_logger(__name__)


async def select_workout(
    session: AsyncSession,
    user: User,
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    try:
        groups = await workout_crud.get_groups(session, user)
    except NoWorkoutsException:
        return (
            await get_banner(OOPS, level),
            get_oops_kb(level=level, menu_name=menu_name),
        )
    return (
        await get_banner(menu_name),
        get_workout_select_btns(level=level, groups=groups),
    )


async def workouts(
    session: AsyncSession,
    level: int,
    menu_name: str,
    workout_group: int,
    page: int,
) -> tuple[InputMediaVideo, InlineKeyboardMarkup]:
    try:
        exercises = await workout_crud.get_exercises(session, workout_group)
    except NoExerciseException:
        return (
            await get_banner(OOPS, level),
            get_oops_kb(level=level, menu_name=menu_name),
        )
    pagination = Paginator(exercises, page)
    exercise = pagination.get_page()[0]
    video = InputMediaVideo(
        media=FSInputFile(exercise.exercise.video),
        caption=(
            f'<b>{exercise.exercise.name}:</b>\n'
            f'{exercise.exercise.description}'
        ),
    )
    keyboard = get_exercise_btns(
        level=level,
        menu_name=menu_name,
        workout_group=workout_group,
        page=page,
        pagination_btns=get_pages(pagination),
    )
    return video, keyboard
