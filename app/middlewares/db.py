"""Модуль сессии БД."""

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker


class DbSessionMiddleware(BaseMiddleware):
    """Класс сессии БД."""

    def __init__(self, session_pool: async_sessionmaker) -> None:
        """Инициализация сессии."""
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Awaitable:
        """Вызов сессии."""
        async with self.session_pool() as session:
            data['session'] = session
            return await handler(event, data)
