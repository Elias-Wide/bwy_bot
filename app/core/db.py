from typing import AsyncGenerator, TypeVar

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings

Self = TypeVar("Self", bound="PreBase")


class PreBase:

    @declared_attr
    def __tablename__(self: Self) -> str:
        return self.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator:
    async with AsyncSessionLocal() as async_session:
        yield async_session
