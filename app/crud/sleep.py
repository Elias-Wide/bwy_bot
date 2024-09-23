"""CRUD операции относящийся к участку сна."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import SECONDS_IN_HOUR, SleepMode
from app.crud.base import CRUDBase
from app.models import Sleep, User

SLEEP_MODEL_ATRIBUTE = {
    SleepMode.GO_TO_BED: Sleep.go_to_bed_time,
    SleepMode.WAKE_UP: Sleep.wake_up_time,
}


class CRUDSleep(CRUDBase):
    """Класс CRUD операций относящиеся к участку сна."""

    @staticmethod
    async def get_user_sleep_objs(
        user: User,
        limit: int,
        session: AsyncSession,
    ) -> list[Sleep]:
        """
        Запрос для получения записей сна пользователя.

        Передается объект пользователя, который запрашивает
        статистику своего сна и параметр
        limit - возвращаемое количество записей сна.
        """
        sleep_objs = await session.execute(
            select(Sleep)
            .order_by(Sleep.wake_up_time.desc())
            .limit(limit)
            .where(
                Sleep.user_id == user.id,
                Sleep.sleep_duration > 0,
            ),
        )
        return sleep_objs

    @staticmethod
    async def exist_today_sleep(
        session: AsyncSession,
        user: User,
        sleep_status: str,
        utc_offset_hours: int,
    ) -> Sleep:
        """
        Запрос в базу данных на получение объекта записи сна.

        В функцию передается объект пользователя, выполняющего запрос и
        статус сна, который определяет сравниваемые в запросе параметры
        go_to_bed - статус при попытке записать данные ухода ко сну,
        wake_up - статус при попытке записать данные сна,
        когда пользователь проснулся.
        """
        sleep = await session.scalars(
            select(Sleep)
            .where(
                and_(
                    Sleep.user_id == user.id,
                    func.date(SLEEP_MODEL_ATRIBUTE[sleep_status])
                    == func.date(
                        datetime.now(
                            timezone(timedelta(hours=utc_offset_hours)),
                        ),
                    ),
                ),
            )
            .order_by(SLEEP_MODEL_ATRIBUTE[sleep_status].desc()),
        )
        return sleep.first()

    @staticmethod
    async def set_wake_up_time(
        session: AsyncSession,
        user: User,
        wake_up_time: datetime,
    ) -> None:
        """
        Запрос в базу данных для установки времени пробуждения.

        Находит крайнюю запись сна и вычисляет, сколько
        времени пользователь спал, устаналивает время подъема и время сна.
        """
        sleep = await session.scalars(
            select(Sleep)
            .where(
                Sleep.user_id == user.id,
            )
            .order_by(Sleep.go_to_bed_time.desc()),
        )
        sleep = sleep.first()
        wake_up_time = wake_up_time.replace(tzinfo=None)
        duration = wake_up_time - sleep.go_to_bed_time
        duration_in_s = duration.total_seconds()
        sleep.wake_up_time = wake_up_time
        sleep.sleep_duration = duration_in_s / SECONDS_IN_HOUR
        await session.commit()
        return sleep

    @staticmethod
    async def get_last_sleep_obj(
        session: AsyncSession,
        user: User,
    ) -> Sleep:
        """
        Запрос в базу данных получения последнего объекта сна.

        По id пользователя находит последний созданный объект сна, сортировка
        по времени, когда пользователь лег спать.
        """
        sleep = await session.scalars(
            select(Sleep)
            .where(
                and_(
                    Sleep.user_id == user.id,
                ),
            )
            .order_by(Sleep.go_to_bed_time.desc()),
        )
        sleep = sleep.first()
        return sleep


sleep_crud = CRUDSleep(Sleep)
