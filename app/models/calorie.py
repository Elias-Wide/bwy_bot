"""Классы, описывающие модели модуля контроля калорий."""

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import Column
from sqlalchemy_utils import ChoiceType

from app.core.config import STATIC_DIR
from app.core.constants import ACTIVITY_PURPOSE, GENDER, PHYSICAL_ACTIVITY
from app.core.db import Base

storage = FileSystemStorage(path=STATIC_DIR)


class Calorie(Base):
    """Класс-описание модели контроля калорий.

    Args:
        gender: пол
        purpose: цель тренировок
        activity: физическая активность
        pucture: картинка
    """

    gender = Column(ChoiceType(GENDER))
    purpose = Column(ChoiceType(ACTIVITY_PURPOSE))
    activity = Column(ChoiceType(PHYSICAL_ACTIVITY))
    picture = Column(FileType(storage=storage))

    def __str__(self) -> str:
        """Строковое представление экземпляра класса."""
        return f' Калории для {self.gender} - {self.activity }'
