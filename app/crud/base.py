from typing import Any, Optional, Sequence

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model: BaseModel) -> None:
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> Any | None:
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id),
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession) -> Sequence:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in: object,
        session: AsyncSession,
        user: Optional[User] = None,
    ) -> object:
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: object,
        obj_in: object,
        session: AsyncSession,
    ) -> object:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: object,
        session: AsyncSession,
    ) -> object:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
    ) -> Any | None:
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value),
        )
        return db_obj.scalars().first()
