"""Модуль утилит.

Functions:
    get_banner: получить баннер для меню
    calculation_of_calories: получить норму калорий для пользователя
"""

from aiogram.types import FSInputFile, InputMediaPhoto
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
    REMINDER_STATE_FALSE,
    REMINDER_STATE_TRUE,
    STATE_CALORIES,
    STATE_SLEEP,
    STATE_TRAIN,
    WEIGHT_COEF_MAN,
    WEIGHT_COEF_WOMAN,
    SleepMode,
)
from app.crud import schedule_crud
from app.models import User
from app.utils.sleep import (
    get_sleep_duration,
    get_sleep_statistic_answer,
    go_to_bed_time,
    wake_up_time,
)


async def get_banner(
    menu_name: str,
    level: int | None = None,
    utc_offset_hours: int | None = None,
) -> InputMediaPhoto:
    """Получить баннер к сообщению.

    Возвращает баннер, соответствующий названию меню и уровню,
    а также описание к нему.

    Args:
        menu_name (str): название меню
        level (int | None, optional): уровень меню
        utc_offset_hours (int | None, optional): разница во времени от UTC

    Returns:
        InputMediaPhoto: изображение к разделу меню, включая описание
    """
    match menu_name:
        case SleepMode.GO_TO_BED:
            caption_text = go_to_bed_time(utc_offset_hours)
        case SleepMode.WAKE_UP:
            caption_text = wake_up_time(utc_offset_hours)
        case SleepMode.DURATION:
            caption_text = get_sleep_duration()
        case SleepMode.STATISTIC:
            caption_text = get_sleep_statistic_answer()
        case _:
            caption_text = (
                CAPTIONS[menu_name][level] if level else CAPTIONS[menu_name]
            )

    return InputMediaPhoto(
        media=FSInputFile(STATIC_DIR.joinpath(menu_name + FMT_JPG)),
        caption=caption_text,
    )


async def calculation_of_calories(user: User) -> float:
    """Вычислить норму калорий.

    Вычисляет норму калорий для пользователя в соответствии с его
    полом, физическими данными и физической активностью.
    Args:
        user (User): объект ользователя

    Returns:
        float: норма каллорий пользователя
    """
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
    """Получить состояние переключателей напоминаний.

    Возвращает состояние переключателей дял конкретного пользователя
    в меню напоминаний.
    STATE_TRAIN - напоминание о тренировке
    STATE_SLEEP - напоминание о сне
    STATE_CALORIES - напоминание о приеме пищи

    Args:
        user (User): объект пользователя
        session (AsyncSession): асинхроннная сессия

    Returns:
        str: строка, содержащая статус (ВКЛ|ВЫКЛ) для всех напоминаний
    """
    schedule = await schedule_crud.get_by_attribute(
        'user_id',
        str(user.id),
        session,
    )
    if getattr(schedule, 'stop_reminder_train'):
        state_train = f'{STATE_TRAIN} - {REMINDER_STATE_TRUE}'
    else:
        state_train = f'{STATE_TRAIN} - {REMINDER_STATE_FALSE}'
    if getattr(schedule, 'stop_reminder_sleep'):
        state_sleep = f'{STATE_SLEEP} - {REMINDER_STATE_TRUE}'
    else:
        state_sleep = f'{STATE_SLEEP} - {REMINDER_STATE_FALSE}'
    if getattr(schedule, 'stop_reminder_calories'):
        state_calories = f'{STATE_CALORIES} - {REMINDER_STATE_TRUE}'
    else:
        state_calories = f'{STATE_CALORIES} - {REMINDER_STATE_FALSE}'
    return f'{state_train}\n' f'{state_sleep}\n' f'{state_calories}\n'
