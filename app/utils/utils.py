from aiogram.types import FSInputFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import BASE_DIR, UPLOAD_DIR
from app.core.constants import (
    ACTIVITY_PURPOSE,
    AGE_COEF_MAN,
    AGE_COEF_WOMAN,
    CAL_COEF_MAN,
    CAL_KOEF_WOMAN,
    COEF_ADD_MASS,
    COEF_ROUND,
    COEF_TO_SLIM,
    GENDER,
    HEIGHT_COEF_MAN,
    HEIGHT_COEF_WOMAN,
    PHYS_ACTIV_KOEF,
    WEIGHT_COEF_MAN,
    WEIGHT_COEF_WOMAN,
)
from app.core.logging import get_logger
from app.models import Calorie, Schedule, User

logger = get_logger(__name__)


async def _get_videos() -> list[FSInputFile]:
    return [FSInputFile(path) for path in list(UPLOAD_DIR.glob('*.mp4'))]


# TODO: exception.TelegramBadRequest: PHOTO_INVALID_DIMENSIONS
async def _get_banner(menu_name: str) -> FSInputFile:
    return FSInputFile(BASE_DIR.joinpath('static', menu_name + '.jpg'))


async def get_calorie_plot(user: User, session: AsyncSession) -> FSInputFile:
    path = await session.scalar(
        select(Calorie.picture).where(
            Calorie.gender == user.gender,
            Calorie.purpose == user.purpose,
            Calorie.activity == user.activity,
        ),
    )
    return FSInputFile(path)


async def calculation_of_calories(user: User) -> float:
    if user.gender == GENDER[0][0]:
        res = (
            CAL_COEF_MAN
            + (WEIGHT_COEF_MAN * user.weight)
            + (HEIGHT_COEF_MAN * user.height)
            - (AGE_COEF_MAN * user.age)
        )
    else:
        res = (
            CAL_KOEF_WOMAN
            + (WEIGHT_COEF_WOMAN * user.weight)
            + (HEIGHT_COEF_WOMAN * user.height)
            - (AGE_COEF_WOMAN * user.age)
        )
    if user.purpose == ACTIVITY_PURPOSE[0][0]:
        return round(
            res * PHYS_ACTIV_KOEF[user.activity] * COEF_TO_SLIM,
            COEF_ROUND,
        )
    elif user.purpose == ACTIVITY_PURPOSE[1][0]:
        return round(res * PHYS_ACTIV_KOEF[user.activity], COEF_ROUND)
    else:
        return round(
            res * PHYS_ACTIV_KOEF[user.activity] * COEF_ADD_MASS,
            COEF_ROUND,
        )


async def get_reminder_state(user: User, session: AsyncSession) -> str:
    statement = select(
        Schedule.stop_reminder_train,
        Schedule.stop_reminder_sleep,
        Schedule.stop_reminder_calories,
    ).where(Schedule.user_id == user.id)
    results = await session.execute(statement)
    human_res = list()
    for res in results:
        for state in list(res):
            if state:
                state = 'Выкл'
            else:
                state = 'Вкл'
            human_res.append(state)
            logger.info(human_res)

    return f'НАПОМИНАЛКИ:\n(тренинг, сон, калории)\n СОСТОЯНИЕ:\n{human_res}'
