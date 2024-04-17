from aiogram.types import (
    FSInputFile,
    InputMediaPhoto,
    InputMediaVideo,
    InlineKeyboardMarkup
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import workout_crud
from app.keyboards import get_workout_select_btns, get_exercise_btns
from app.utils.pagination import Paginator, _get_pages
from app.utils.utils import _get_banner


async def workout_category_menu(
    session: AsyncSession,
    user_id: int,
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Генератор меню выбора группы тренировки."""
    groups = await workout_crud.get_groups(session, user_id)
    return (
        InputMediaPhoto(
            media=await _get_banner(menu_name),
            caption='Какой вид тренировки предпочитаете?',
        ),
        get_workout_select_btns(level=level, groups=groups),
    )


async def workouts(
    session: AsyncSession,
    level: int,
    workout_group: int,
    page: int,
) -> tuple[InputMediaVideo, InlineKeyboardMarkup]:
    exercises = await workout_crud.get_exercises(session, workout_group)
    pagination = Paginator(exercises, page)
    exercise = pagination.get_page()[0]
    print(exercise.video)
    video = FSInputFile(path=str(exercise.video))
    video = InputMediaVideo(
        media=video,
        caption=f'<b>{exercise.name}:</b>\n{exercise.description}'
    )
    pagination_btns = _get_pages(pagination)
    keyboard = get_exercise_btns(
        level=level,
        workout_group=workout_group,
        page=page,
        pagination_btns=pagination_btns,
    )

    return video, keyboard
