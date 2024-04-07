from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from typing import TypeVar, Union, Literal
from sqlalchemy import Enum, Column, String
from pydantic import BaseModel, Field
from sqlalchemy_utils import ChoiceType


from app.core.db import Base

Self = TypeVar("Self", bound="User")

GENDER = [
    ('admin', 'Admin'),
    ('regular-user', 'Regular user')
]


class User(SQLAlchemyBaseUserTable[int], Base):
    GENDER = (
        ('Male', 'Мужчина'),
        ('Female', 'Женщина')
    )
#    gender = Column(String(7), unique=False, nullable=True)
    gender = Column(ChoiceType(GENDER))
#    Column(ChoiceType({"short": "short", "medium": "medium", "tall": "tall"}), nullable=False)
#    gender = Column(Gender, default=Gender.Male)
    #name = Column(String(100), unique=True, nullable=False)

    def __str__(self: Self) -> str:
        return f' #{self.id}  {self.email}'
