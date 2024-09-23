"""Модуль утилит для напоминаний."""

from datetime import datetime, timezone

from app.crud import schedule_crud


async def get_timedeltas_from_constant_time(
    time_remainders_from_constant: str,
) -> tuple[int, ...]:
    """Метод для вычисления timedelta, кому пора отправлять напоминания."""
    utc_now = int(datetime.now(tz=timezone.utc).hour)
    timedelta_to_reminder = tuple(
        (int(x) - utc_now) * 3600
        for x in time_remainders_from_constant.split(',')
    )
    return timedelta_to_reminder


async def get_active_adv_hour() -> str:
    """Метод возвращает строку с временем напоминания активных анонсов."""
    return await schedule_crud.get_act_adv_hour()
