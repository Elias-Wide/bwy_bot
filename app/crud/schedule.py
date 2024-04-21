from datetime import datetime
from typing import TypeVar

from fastapi_sqlalchemy import db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DIET, SLEEP, WORKOUTS
from app.core.logging import get_logger
from app.crud.base import CRUDBase
from app.crud.user import user_crud
from app.models import Schedule, User

ModelType = TypeVar('ModelType', bound=CRUDBase)


logger = get_logger(__name__)


class CRUDSchdeule(CRUDBase):

    async def get_telegram_id(self, stop_reminder: str) -> list:
        """Метод для возврата telegram id в зависимости от напоминания."""
        if stop_reminder == WORKOUTS:
            schedule_reminder = Schedule.stop_reminder_train.is_(False)
        elif stop_reminder == DIET:
            schedule_reminder = Schedule.stop_reminder_calories.is_(False)
        elif stop_reminder == SLEEP:
            schedule_reminder = Schedule.stop_reminder_sleep.is_(False)

        with db():
            users_id = db.session.scalars(
                select(
                    User.telegram_id,
                ).where(
                    User.id == Schedule.user_id,
                    schedule_reminder,
                ),
            )
            return users_id.all()

    async def switch_reminder(
        self,
        telegram_id: int,
        stop_reminder_field: bool,
        session: AsyncSession,
    ) -> ModelType | None:
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


schedule_crud = CRUDSchdeule(Schedule)
