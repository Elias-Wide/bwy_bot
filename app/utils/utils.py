from aiogram.types import FSInputFile

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import BASE_DIR, UPLOAD_DIR
from app.core.constants import PHYS_ACTIV_KOEF
from app.models.user import User
from app.models.calorie import Calorie


async def _get_videos() -> list[FSInputFile]:
    return [FSInputFile(path) for path in list(UPLOAD_DIR.glob('*.mp4'))]


# TODO: exception.TelegramBadRequest: PHOTO_INVALID_DIMENSIONS
async def _get_banner(menu_name: str) -> FSInputFile:
    return FSInputFile(BASE_DIR.joinpath('static', menu_name + '.jpg'))


async def _get_calorie_plot(user: User, session: AsyncSession) -> FSInputFile:
    plot = await session.execute(select(Calorie.picture).where(
        Calorie.gender == user.gender,
        Calorie.purpose == user.purpose,
        Calorie.activity == user.activity))
    path = plot.scalars().first()
    return FSInputFile(path)


async def _calculation_of_calories(user: User) -> float:
    if user.gender == 'MALE':
        res = (88.36 + (13.4 * user.weight)
               + (4.8 * user.height) - (5.7 * user.age))
    else:
        res = (447.6 + (9.2 * user.weight)
               + (3.1 * user.height) - (4.3 * user.age))
    if user.purpose == 'GO_SLIM':
        return round(res * PHYS_ACTIV_KOEF[user.activity] * 0.85, 2)
    elif user.purpose == 'KEEP_LEVEL':
        return round(res * PHYS_ACTIV_KOEF[user.activity], 2)
    else:
        return round(res * PHYS_ACTIV_KOEF[user.activity] * 1.2, 2)
