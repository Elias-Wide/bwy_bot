from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.crud.base import CRUDBase
from app.exceptions.calorie import NoCaloriePlot
from app.models import User, Calorie

logger = get_logger(__name__)


class CalorieCRUD(CRUDBase):

    @staticmethod
    async def get_plot(session: AsyncSession, user: User) -> str:
        plot = await session.scalar(select(Calorie.picture).where(
            Calorie.gender == user.gender,
            Calorie.purpose == user.purpose,
            Calorie.activity == user.activity,
        ),
        )
        if not plot:
            logger.error(
                'В базе для %s, %s и %s нет графика.',
                user.gender,
                user.purpose,
                user.activity,
            )
            raise NoCaloriePlot()

        return plot


calorie_crud = CalorieCRUD(Calorie)
