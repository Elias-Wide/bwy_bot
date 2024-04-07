from fastapi_users import schemas
from app.models.user import Gender
from typing import Optional


class UserRead(schemas.BaseUser[int]):
    gender: Gender


class UserCreate(schemas.BaseUserCreate):
    gender: Gender


class UserUpdate(schemas.BaseUserUpdate):
    gender: Gender
