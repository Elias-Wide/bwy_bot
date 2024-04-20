from aiogram.types import FSInputFile, InputMediaPhoto
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import BASE_DIR, STATIC_DIR, UPLOAD_DIR
from app.core.constants import (
    ACTIVITY_PURPOSE,
    AGE_COEF_MAN,
    AGE_COEF_WOMAN,
    CAL_COEF_MAN,
    CAL_KOEF_WOMAN,
    CAPTIONS,
    COEF_ADD_MASS,
    COEF_ROUND,
    COEF_TO_SLIM,
    FMT_JPG,
    GENDER,
    HEIGHT_COEF_MAN,
    HEIGHT_COEF_WOMAN,
    PHYS_ACTIV_KOEF,
    WEIGHT_COEF_MAN,
    WEIGHT_COEF_WOMAN,
    STATE_TRAIN,
    STATE_SLEEP,
    STATE_CALORIES,
    REMINDER_STATE_TRUE,
    REMINDER_STATE_FALSE,
)
from app.core.logging import get_logger
from app.crud import schedule_crud
from app.models import Calorie, Schedule, User

logger = get_logger(__name__)


# TODO: exception.TelegramBadRequest: PHOTO_INVALID_DIMENSIONS
async def get_banner(
    menu_name: str,
    level: int | None = None,
) -> InputMediaPhoto:
    return InputMediaPhoto(
        media=FSInputFile(STATIC_DIR.joinpath(menu_name + FMT_JPG)),
        caption=CAPTIONS[menu_name][level] if level else CAPTIONS[menu_name],
    )


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
    schedule_state = await schedule_crud.get(user.id, session)
    if schedule_state.__getattribute__('stop_reminder_train'):
        state_train = f'{STATE_TRAIN} - {REMINDER_STATE_TRUE}'
    else:
        state_train = f'{STATE_TRAIN} - {REMINDER_STATE_FALSE}'
    if schedule_state.__getattribute__('stop_reminder_sleep'):
        state_sleep =  f'{STATE_SLEEP} - {REMINDER_STATE_TRUE}'
    else:
        state_sleep =  f'{STATE_SLEEP} - {REMINDER_STATE_FALSE}'
    if schedule_state.__getattribute__('stop_reminder_calories'):
        state_calories = f'{STATE_CALORIES} - {REMINDER_STATE_TRUE}'
    else:
        state_calories =  f'{STATE_CALORIES} - {REMINDER_STATE_FALSE}'

    return (
        f'{state_train}\n'
        f'{state_sleep}\n'
        f'{state_calories}\n'
    )
