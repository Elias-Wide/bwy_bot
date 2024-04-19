from datetime import datetime

from aiogram.types import FSInputFile, InputMediaPhoto
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import STATIC_DIR
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
)
from app.models import Calorie, User

from .const import USER_DATE_FORMAT


# TODO: exception.TelegramBadRequest: PHOTO_INVALID_DIMENSIONS
async def get_banner(
    menu_name: str,
    level: int | None = None,
) -> InputMediaPhoto:
    return InputMediaPhoto(
        media=FSInputFile(STATIC_DIR.joinpath(menu_name + FMT_JPG)),
        caption=CAPTIONS[menu_name][level] if level else CAPTIONS[menu_name],
    )


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


async def go_to_bed_time() -> str:
    return (
        'Ваше время отхода ко сну:'
        f' {datetime.now().strftime(USER_DATE_FORMAT)}'
    )


async def wake_up_time() -> str:
    return f'Вы проснулись в: {datetime.now().strftime(USER_DATE_FORMAT)}'


async def get_sleep_duration() -> str:
    sleep_duration = 8.5  # TODO вычислять
    if not sleep_duration:
        sleep_duration = 8
        return (
            f'Сегодня ночью Вы спали: {sleep_duration} часов? '
            'Ответьте Да или Нет. Мы запишем Ваши данные о сне '
        )
    if sleep_duration >= 8:
        return (
            f'Сегодня ночью Вы спали: {sleep_duration} часов? '
            'Зоровый образ жизни прежде всего. '
            'Нажмите Да. Мы запишем Ваши данные о сне '
        )
    return (
        f'Сегодня ночью Вы спали: {sleep_duration} часов? '
        'Нажмите Нет. Это не достаточное количество сна.'
        'Мы запишем Ваши данные о сне. '
        'Напоминаем, рекомендуется спать не менее 8.'
    )


async def get_sleep_statistic() -> str:
    sleep_week_duration = (  # TODO вычислять
        'Коротко о Вашем сне:\n\n'
        'вчера не менее 8 часов, \n'
        'позавчера не менее 8 часов, \n'
        '16.04.2024 не менее 8 часов, \n'
        '15.04.2024 МЕНЕЕ 8 часов, \n'
        '14.04.2024 МЕНЕЕ 8 часов, \n'
        '13.04.2024 не менее 8 часов, \n'
        '12.04.2024 не менее 8 часов \n\n'
    )
    return sleep_week_duration
