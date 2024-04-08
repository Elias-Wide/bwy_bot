from typing import TypeVar

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import ChoiceType

from app.core.constants import ACTIVITY_PURPOSE, GENDER
from app.core.db import Base

Self = TypeVar("Self", bound=None)


class User(SQLAlchemyBaseUserTable[int], Base):
    telegram_id = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    gender = Column(ChoiceType(GENDER))
    age = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    activity = Column(ChoiceType(ACTIVITY_PURPOSE))

    def __str__(self: Self) -> str:
        return f' #{self.id}  {self.email}'
