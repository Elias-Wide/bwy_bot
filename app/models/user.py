from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from app.core.constants import (ACTIVITY_PURPOSE,
                                GENDER,
                                PHYSICAL_ACTIVITY)
from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    telegram_id = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    gender = Column(ChoiceType(GENDER))
    age = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    activity = Column(ChoiceType(PHYSICAL_ACTIVITY))
    purpose = Column(ChoiceType(ACTIVITY_PURPOSE))

    sleep = relationship('Sleep', back_populates='user')
    schedule = relationship('Schedule', back_populates='user')

    def __str__(self) -> str:
        return f'{self.id}  {self.email}'
