"""Классы, описывающие таблицы БД планировщика."""

from datetime import datetime
from typing import Any

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from app.core.config import STATIC_DIR
from app.core.constants import (
    GENDER_NOT_SELECTED,
    GENDER_OR_NONE,
    SOME_ADV_TEXT,
)
from app.core.db import AsyncSessionLocal, Base


class BaseMixin(object):
    """
    Вспомогательный класс.

    Можно при создании экемпляра
    указывать в параметре значение.
    """

    @classmethod
    async def create(cls, **kw: dict[str, Any]) -> None:
        """
        Метод позволяющий создавать объект и присваивать значение.

        При создании через параметр указывается значение.
        schedule_crud.create(
            Schedule(utc_offset=utc_offset),
        )
        """
        obj = cls(**kw)
        async with AsyncSessionLocal() as session:
            session.add(obj)
            session.commit()


class Schedule(BaseMixin, Base):
    """
    Класс, описывающий таблицу напоминаний пользователя.

    Cодержит расписание функциональных напоминаний пользователю
    о тренировках, контроле калорий и контроле сна.
    """

    user_id = Column(Integer, ForeignKey('user.id'))
    start_course = Column(DateTime, default=datetime.now)
    stop_reminder_train = Column(Boolean, default=False)
    stop_reminder_sleep = Column(Boolean, default=False)
    stop_reminder_calories = Column(Boolean, default=False)
    stop_reminder_adv = Column(Boolean, default=False)
    utc_offset = Column(Integer, default=None)

    user = relationship('User', back_populates='schedule', uselist=False)

    def __init__(self, utc_offset: Column[int]) -> None:
        """Инициализация экземпляра класса."""
        self.utc_offset = utc_offset

    def __str__(self) -> str:
        """Строковое представление экземпляра класса."""
        return f'Пользователь с id {self.user_id} старт в {self.start_course }'


class Advertisement(Base):
    """
    Класс, описывающий таблицу рекламных анонсов.

    Содержит расписание рекламных объявлений пользователям.
    """

    name = Column(
        String(128),
        unique=True,
        nullable=False,
        default='Name of schedule job',
    )
    text = Column(String(1024), unique=False, default=SOME_ADV_TEXT)
    image = Column(FileType(storage=FileSystemStorage(path=STATIC_DIR)))
    hour_to_adv = Column(Integer, nullable=False, default=11)
    active = Column(Boolean, default=False)
    gender = Column(ChoiceType(GENDER_OR_NONE), default=GENDER_NOT_SELECTED)

    __table_args__ = (
        UniqueConstraint(
            'hour_to_adv',
            'active',
            name='unique_hour_and_active',
        ),
        CheckConstraint(
            '(8<hour_to_adv) and (hour_to_adv<21)',
            name='check_min_max_hour',
        ),
    )
