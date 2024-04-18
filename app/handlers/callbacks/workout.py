from aiogram.types import (
    FSInputFile,
    InputMediaPhoto,
    InputMediaVideo,
    InlineKeyboardMarkup
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import workout_crud
from app.exceptions.workout import NoExerciseException, NoWorkoutsException
from app.keyboards import (
    get_workout_select_btns,
    get_exercise_btns,
    get_oops_kb
)
from app.utils.pagination import Paginator, _get_pages
from app.utils.utils import _get_banner


async def workout_category_menu(
    session: AsyncSession,
    user_id: int,
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Генератор меню выбора группы тренировки."""
    try:
        groups = await workout_crud.get_groups(session, user_id)
    except NoWorkoutsException:
        return (
            await _get_banner('oops', level),
            get_oops_kb(level=level, menu_name=menu_name)
        )
    return (
        await _get_banner(menu_name),
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
            await _get_banner('oops', level),
            get_oops_kb(level=level, menu_name=menu_name)
    )

    pagination = Paginator(exercises, page)
    exercise = pagination.get_page()[0]
    video = InputMediaVideo(
        media=FSInputFile(str(exercise.exercise.video)),
        caption=f'<b>{exercise.exercise.name}:</b>\n{exercise.exercise.description}'
    )
    keyboard = get_exercise_btns(
        level=level,
        workout_group=workout_group,
        page=page,
        pagination_btns=_get_pages(pagination),
    )

    return video, keyboard
