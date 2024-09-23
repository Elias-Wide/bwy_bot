"""Модуль утилит для вступительной анкеты.

Functions:
    get_timezone_from_location: получить часовой пояс по локации
    get_utc_offset: получить разницу во времени от UTC в секундах
    get_possible_location: получить возможную локацию пользователя
"""

import datetime
import random

import pytz
import timezonefinder

from app.core.constants import TIMEZONE_RU


async def get_timezone_from_location(lng: float, lat: float) -> str | None:
    """Получить часовой пояс по геолокации.

    По долготе и широте определяет временной пояс.

    Args:
        lng (float): долгота
        lat (float): широта

    Returns:
        str | None: часовой пояс
    """
    tf = timezonefinder.TimezoneFinder()
    timezone_str = tf.certain_timezone_at(lng=lng, lat=lat)
    return timezone_str


async def get_utc_offset(timezone_str: str) -> float:
    """Получить разницу во времени от UTC в секундах."""
    try:
        timezone = pytz.timezone(timezone_str)
    except Exception:
        timezone = pytz.timezone('Europe/Moscow')
    else:
        dt = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    return timezone.utcoffset(dt).total_seconds()


async def get_possible_location(
    message_text: str,
    message_date: datetime.datetime,
) -> str:
    """Получить возможную локацию.

    Передается время в строковом формате, по нему определяется возможная
    локация.
    """
    text_hour = int(message_text.split(':')[0])
    date_hour = int(message_date.strftime("%H:%M").split(':')[0])
    if date_hour < text_hour:
        hours = text_hour - date_hour
    else:
        hours = 24 - date_hour + text_hour
    try:
        tzone = TIMEZONE_RU[hours]
    except Exception:
        if date_hour < text_hour:
            hours = text_hour - 24 - date_hour
        else:
            hours = text_hour - date_hour
        utc_offset = datetime.timedelta(hours=hours)

        random_location = {
            tz.zone
            for tz in map(pytz.timezone, pytz.all_timezones_set)
            if message_date.astimezone(tz).utcoffset() == utc_offset
        }
        tzone = list(random_location)[
            random.randrange(0, len(random_location))
        ]
    return tzone
