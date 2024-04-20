from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.crud.base import CRUDBase
from app.models import Schedule, User


class CRUDSchdeule(CRUDBase):

    async def get_telegram_id(self, stop_reminder: str) -> list:
        """Метод для возврата telegram id в зависимости от напоминания."""
        stmt = select(User.telegram_id).where(User.id == Schedule.user_id)

        match stop_reminder:
            case 'workouts':
                stmt = stmt.where(Schedule.stop_reminder_train.is_(False))
            case 'diet':
                stmt = stmt.where(Schedule.stop_reminder_calories.is_(False))
            case 'sleep':
                stmt = stmt.where(Schedule.stop_reminder_sleep.is_(False))

        async with AsyncSessionLocal() as session:
            users_id = await session.scalars(stmt)
            return users_id.all()


schedule_crud = CRUDSchdeule(Schedule)
