"""Схемы пользователя."""

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема чтения пользователя."""

    pass


class UserCreate(schemas.BaseUserCreate):
    """Схема создания пользователя."""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Схема обновления пользователя."""

    pass
