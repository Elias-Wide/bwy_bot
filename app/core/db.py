"""Настройки для работы с БД."""

from typing import AsyncGenerator

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """Родительский класс для базового."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Возвращает имя для таблицы в нижнем регистре."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator:
    """Получение асинхронной сессии."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
