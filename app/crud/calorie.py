"""CRUD операции относящиеся к участку питание."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DIET_CRUD_ERROR
from app.core.logging import get_logger
from app.crud.base import CRUDBase
from app.exceptions.calorie import NoCaloriePlot
from app.models import Calorie, User

logger = get_logger(__name__)


class CalorieCRUD(CRUDBase):
    """Класс CRUD операций относящиеся к участку питание."""

    @staticmethod
    async def get_plot(session: AsyncSession, user: User) -> str:
        """Возвращает путь к файлу нужной картинки."""
        plot = await session.scalar(
            select(Calorie.picture).where(
                Calorie.gender == user.gender,
                Calorie.purpose == user.purpose,
                Calorie.activity == user.activity,
            ),
        )
        if not plot:
            logger.error(
                DIET_CRUD_ERROR,
                user.gender,
                user.purpose,
                user.activity,
            )
            raise NoCaloriePlot()

        return plot


calorie_crud = CalorieCRUD(Calorie)
