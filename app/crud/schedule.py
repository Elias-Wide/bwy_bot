from fastapi_sqlalchemy import db
from sqlalchemy import select

from app.core.constants import DIET, SLEEP, WORKOUTS
from app.crud.base import CRUDBase
from app.models import Schedule, User


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
                select(User.telegram_id).where(
                    User.id == Schedule.user_id,
                    schedule_reminder,
                ),
            )
            return users_id.all()


schedule_crud = CRUDSchdeule(Schedule)
