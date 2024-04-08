from fastapi_users import schemas
from app.core.constants import GENDER, ACTIVITY_PURPOSE
from typing import Optional
from pydantic import Field, PositiveInt
from sqlalchemy import Integer


class UserRead(schemas.BaseUser[int]):
    # gender: GENDER
    # telegram_id: Optional[PositiveInt]
    # name: Optional[str] = Field(None, min_length=1, max_length=100)
    # age: Optional[Integer]
    # weight: Optional[Integer]
    # height: Optional[Integer]
    # activity: ACTIVITY_PURPOSE
    pass

class UserCreate(schemas.BaseUserCreate):
    # gender: GENDER
    # telegram_id: Optional[int]
    # name: Optional[str] = Field(None, min_length=1, max_length=100)
    # age: Optional[int]
    # weight: Optional[int]
    # height: Optional[int]
    # activity: ACTIVITY_PURPOSE
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass
