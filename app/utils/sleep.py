"""Модуль утилит для логики сна.

Functions:
    go_to_bed_time: время отхода ко сну
    wake_up_time: время, когда пользователь проснулся
    get_sleep_duration: получить продолжительность сна
    get_sleep_statistic_answer: получить статистику сна
    get_yesterdayЖ получить вчерашнюю дату
    get_default_time: получить дефолтное ('идеальное') время сна
    get_sleep_status: получить статус объекта сна
"""

from datetime import datetime, timedelta, timezone

from app.core.constants import (
    DEFAULT_SLEEP_DURATION,
    GO_TO_BED_TEXT,
    HEALTHY_SLEEP,
    SECONDS_IN_HOUR,
    SET_DEFAULT_SLEEP_DURATION_QUESTION,
    SLEEP_DURATION_QUESTION_TEXT,
    SLEEP_STATISTIC_FORMAT,
    STATISTIC_TITLE_TEXT,
    UNHEALTHY_SLEEP,
    USER_DATE_FORMAT,
    WAKE_UP_TEXT,
    SleepMode,
)
from app.models import Sleep


def go_to_bed_time(utc_offset_hours: int) -> str:
    """Получить время отхода ко сну с коментарием."""
    return (
        f'{GO_TO_BED_TEXT}'
        f'''
        {datetime.now(timezone(timedelta(hours=utc_offset_hours))).strftime(USER_DATE_FORMAT)}
        '''
    )


def wake_up_time(utc_offset_hours: int) -> str:
    """Получить время, когда пользователь проснулся, с коментарием."""
    return (
        f'{WAKE_UP_TEXT}'
        f'''
        {datetime.now(timezone(timedelta(hours=utc_offset_hours))).strftime(USER_DATE_FORMAT)
            }'''
    )


def get_sleep_duration() -> str:
    """получить прожолжительность сна с соответвующим комментарием."""
    return (
        f'{SLEEP_DURATION_QUESTION_TEXT.format(DEFAULT_SLEEP_DURATION)}\n'
        f'{SET_DEFAULT_SLEEP_DURATION_QUESTION}'
    )


def get_sleep_statistic_answer(sleeps: list[Sleep]) -> str:
    """Получить статистику сна.

    Передается список записей сна, где вычислена его продолжительность.
    Формирует строку, содержащую дату - время сна - комментарий.

    Args:
        sleeps (list[Sleep]): список записей сна

    Returns:
        str: строка со статистикой
    """
    res = STATISTIC_TITLE_TEXT
    for sleep_obj in sleeps:
        sleep_status, sleep_duration = HEALTHY_SLEEP, int(
            sleep_obj[0].sleep_duration,
        )
        if sleep_duration < DEFAULT_SLEEP_DURATION:
            sleep_status = UNHEALTHY_SLEEP
        res = res + (
            f'{sleep_obj[0].wake_up_time.strftime(SLEEP_STATISTIC_FORMAT)}'
            f' - {sleep_duration}ч - {sleep_status}\n'
        )
    return res


async def get_yesterday(utc_offset_hours: float) -> datetime:
    """Получить вчерашнуюю дату."""
    return datetime.now(
        timezone(timedelta(hours=utc_offset_hours)),
    ) - timedelta(hours=24)


async def get_default_time(date: datetime, hours: int) -> datetime:
    """Получить дефолтное время сна.

    В идеале человек должен ложииться в 22ч и просыпаться в 7ч.
    Эта функция устаналивает переданное дефолтное значение часов
    в объект datetime и возвращает его.
    Args:
        date (datetime): объекта datetime
        hours (int): часы

    Returns:
        datetime: _description_
    """
    return date.replace(hour=hours, minute=0, second=0, microsecond=0)


async def get_sleep_status(
    sleep: Sleep,
    utc_offset_hours: int,
    code: str,
) -> str:
    """Проверка статуса объекта сна.

    Функция получает объект сна для проверки, также передается код
    в соответствии с хэндлером, откуда вызвана функция.
    Код определяет, по каким критериям проверяется запись сна.
    timestamp - временная отсечка в +15ч к текущей дате,
    после нее нельзя записать время сна кнопкой "Проснулся",
    во второй половине уже необходимо использовать кнопку 'ложусь спать'.
    """
    current_datetime = datetime.now(
        timezone(timedelta(hours=utc_offset_hours)),
    )
    yesterday_date = await get_yesterday(utc_offset_hours)
    yesterday_date = yesterday_date.date()
    today = current_datetime.date()
    timestamp = await get_default_time(current_datetime, 15)
    time_difference = (
        current_datetime.replace(tzinfo=None)
        - sleep.go_to_bed_time.replace(tzinfo=None)
    ).seconds // SECONDS_IN_HOUR
    match code:
        case SleepMode.GO_TO_BED:
            if timestamp > current_datetime:
                return SleepMode.NOT_TIME_GTB
            if (
                sleep.go_to_bed_time.date() == yesterday_date
                and not sleep.wake_up_time
                and current_datetime > timestamp
            ):
                return SleepMode.FORGOT_SET_WKUP_TIME
            if sleep.go_to_bed_time.date() == today:
                if sleep.go_to_bed_time.replace(
                    tzinfo=None,
                ) > timestamp.replace(tzinfo=None):
                    return SleepMode.SLEEP_EXIST
                if not sleep.wake_up_time and current_datetime > timestamp:
                    return SleepMode.FORGOT_SET_WKUP_TIME
            return SleepMode.VALID
        case SleepMode.WAKE_UP:
            if timestamp < current_datetime:
                return SleepMode.NOT_TIME_WKUP
            if time_difference < 4:
                return SleepMode.SLEEP_EXIST
            if (
                (
                    sleep.go_to_bed_time.date() == yesterday_date
                    or sleep.go_to_bed_time.date() == today
                )
                and sleep.wake_up_time
                and timestamp > current_datetime
            ):
                return SleepMode.SLEEP_EXIST
            return SleepMode.VALID
        case SleepMode.DURATION:
            if sleep.go_to_bed_time.date() == today and (
                time_difference < 4 or timestamp > current_datetime
            ):
                return SleepMode.SLEEP_EXIST
            return SleepMode.VALID
