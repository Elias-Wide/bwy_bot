"""Базовые операции по созданию, чтению, обновлению и удалению."""

from typing import Generic, Sequence, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.core.logging import get_logger

logger = get_logger(__name__)

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Класс базовых операций создания, чтения, обновления и удаления."""

    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> ModelType | None:
        """Возвращает объект по заданному id."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id),
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession) -> Sequence:
        """Возврацает все объекты."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    @staticmethod
    async def create(
        obj: ModelType,
        session: AsyncSession,
    ) -> ModelType:
        """Создает объект."""
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @staticmethod
    async def update(
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        session: AsyncSession,
    ) -> ModelType:
        """Обновляет объект."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    @staticmethod
    async def remove(
        db_obj: ModelType,
        session: AsyncSession,
    ) -> ModelType:
        """Удаляет объект."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
    ) -> ModelType | None:
        """Возвращает объект по заданому атрибуту."""
        db_obj = await session.execute(
            select(self.model).where(
                getattr(self.model, attr_name) == attr_value,
            ),
        )
        return db_obj.scalars().first()
