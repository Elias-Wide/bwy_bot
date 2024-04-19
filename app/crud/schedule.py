from typing import Generic, Sequence, Type, TypeVar
from fastapi_sqlalchemy import db
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.crud import user_crud
from app.core.constants import WORKOUTS, DIET, SLEEP
from app.models import Schedule, User
from app.core.logging import get_logger
from fastapi.encoders import jsonable_encoder


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
                    User.telegram_id
                ).where(
                    User.id == Schedule.user_id,
                    schedule_reminder
                )
            )
            return users_id.all()

    async def get_schedule_by_telegram_id(
        self,
        telegram_id,
        session: AsyncSession,
    ):
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
        setattr(schedule, 'stop_reminder_train', True)
        
        # db_obj = await session.execute(
        #     select(Schedule).where(Schedule.user_id == user.id))
        
        # for field, value in db_obj:
        #     logger.info(f'{field} --{value}')
        #     if field == 'stop_reminder_train':
#                setattr(db_obj, 'stop_reminder_train', True)
        session.add(schedule)
        await session.commit()
        await session.refresh(schedule)
        logger.info(f'{telegram_id}--{user.id} -{schedule}')
        return schedule
#        return db_obj.scalars().first()

    async def switch_reminder(self, telegram_id, stop_reminder_checkbox: str) -> bool:
        logger.info(f'{telegram_id}--{stop_reminder_checkbox}')
        return False


schedule_crud = CRUDSchdeule(Schedule)
