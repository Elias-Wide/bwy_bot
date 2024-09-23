"""CRUD операции относящийся к напоминаниям."""

from datetime import datetime
from typing import Any

from sqlalchemy import and_, select, true
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (
    GENDER_NOT_SELECTED,
    GENDER_OR_NONE,
    ScheduleReminder,
)
from app.core.db import AsyncSessionLocal
from app.core.logging import get_logger
from app.crud.base import CRUDBase
from app.crud.user import user_crud
from app.models import Advertisement, Schedule, User

logger = get_logger(__name__)


class CRUDSchdeule(CRUDBase):
    """Класс CRUD относящийся к напоминаниям."""

    async def get_telegram_id(
        self,
        stop_reminder: str,
        timedelta: tuple[int, ...] | int,
        gender: str = GENDER_NOT_SELECTED,
    ) -> list:
        """Метод для возврата telegram id в зависимости от напоминания."""
        stmt = select(User.telegram_id).where(User.id == Schedule.user_id)
        match stop_reminder:
            case ScheduleReminder.WORKOUTS:
                stmt = stmt.where(
                    and_(
                        Schedule.stop_reminder_train.is_(False),
                        Schedule.utc_offset.in_(timedelta),
                    ),
                )
            case ScheduleReminder.DIET:
                stmt = stmt.where(
                    and_(
                        Schedule.stop_reminder_calories.is_(False),
                        Schedule.utc_offset.in_(timedelta),
                    ),
                )
            case ScheduleReminder.SLEEP:
                stmt = stmt.where(
                    and_(
                        Schedule.stop_reminder_sleep.is_(False),
                        Schedule.utc_offset.in_(timedelta),
                    ),
                )
            case ScheduleReminder.ADV:
                if (
                    gender.value
                    is not dict(GENDER_OR_NONE)[GENDER_NOT_SELECTED]
                ):
                    stmt = select(User.telegram_id).where(
                        and_(
                            User.id == Schedule.user_id,
                            User.gender == gender,
                        ),
                    )
                stmt = stmt.where(
                    and_(
                        Schedule.stop_reminder_adv.is_(False),
                        Schedule.utc_offset == timedelta,
                    ),
                )

        async with AsyncSessionLocal() as session:
            users_id = await session.scalars(stmt)
            return users_id.all()

    async def switch_reminder(
        self,
        telegram_id: int,
        stop_reminder_field: str,
        session: AsyncSession,
    ) -> Any | None:
        """Метод для переключения ON - OFF напоминания."""
        user = await user_crud.get_by_attribute(
            'telegram_id',
            telegram_id,
            session,
        )
        schedule = await schedule_crud.get_by_attribute(
            'user_id',
            user.id,
            session,
        )
        if getattr(schedule, stop_reminder_field):
            setattr(schedule, stop_reminder_field, False)
        else:
            setattr(schedule, stop_reminder_field, True)
        if stop_reminder_field == 'stop_reminder_train':
            setattr(schedule, 'start_course', datetime.now())
        session.add(schedule)
        await session.commit()
        await session.refresh(schedule)
        return schedule

    async def get_act_adv_hour(
        self,
    ) -> str:
        """Возвращает строку часами напоминания анонсов."""
        async with AsyncSessionLocal() as session:
            hours = await session.scalars(
                select(Advertisement.hour_to_adv).where(
                    Advertisement.active == true(),
                ),
            )
        return ','.join(str(el) for el in hours.all())

    async def get_adv_by_hour(self, hour: int) -> list:
        """Возвращает gender рекламы."""
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(
                    Advertisement.gender,
                    Advertisement.text,
                    Advertisement.image,
                ).where(Advertisement.hour_to_adv == hour),
            )
            advertisement = result.one_or_none()
        return advertisement


schedule_crud = CRUDSchdeule(Schedule)
