"""Классы, описывабщие модели пользователя."""

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import CheckConstraint, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from app.core.constants import (
    ACTIVITY_PURPOSE,
    ALLOWED_AGE_RANGE,
    ALLOWED_HEIGHT_RANGE,
    ALLOWED_WEIGHT_RANGE,
    GENDER,
    PHYSICAL_ACTIVITY,
)
from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Класс, описывающий модель пользователя в БД."""

    __table_args__ = (
        CheckConstraint('age between (%s, %s)' % ALLOWED_AGE_RANGE),
        CheckConstraint('height between (%s, %s)' % ALLOWED_HEIGHT_RANGE),
        CheckConstraint('weight between (%s, %s)' % ALLOWED_WEIGHT_RANGE),
    )

    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(100), unique=False, nullable=False)
    gender = Column(ChoiceType(GENDER))
    age = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    activity = Column(ChoiceType(PHYSICAL_ACTIVITY))
    purpose = Column(ChoiceType(ACTIVITY_PURPOSE))
    location = Column(String(128), unique=False, default=None)

    sleep = relationship('Sleep', back_populates='user')
    schedule = relationship('Schedule', back_populates='user')

    def __str__(self) -> str:
        """Строковое представление экземпляра класса.

        Возвращет строку, содержащую имя, id, email пользователя.
        """
        return (
            f'{type(self).__name__}: id={self.id},'
            f' name={self.name}, email={self.email}'
        )
