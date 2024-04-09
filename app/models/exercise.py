from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from app.core.constants import (
    ACTIVITY_PURPOSE,
    AM_NOON_PM,
    GENDER,
    WORKOUT_TYPE,
)
from app.core.db import Base

storage = FileSystemStorage(path='./upload')


class Exercise(Base):

    name = Column(String(255), unique=True, nullable=False)
    descriptin = Column(Text, nullable=False)
    video = Column(FileType(storage=storage))
    workout_type = Column(ChoiceType(WORKOUT_TYPE))

    course = relationship('Course', back_populates='exercise')

    def __str__(self) -> str:
        return f' #{self.name}'


class Course(Base):
    gender = Column(ChoiceType(GENDER))
    activity = Column(ChoiceType(ACTIVITY_PURPOSE))
    corse_day = Column(Integer)
    am_noon_pm = Column(ChoiceType(AM_NOON_PM))
    exercise_id = Column(Integer, ForeignKey('exercise.id'))

    exercise = relationship('Exercise', back_populates='course')

    def __str__(self) -> str:
        return f' #{self.gender} + {self.activity}'


class Shedule(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    start_course = Column(DateTime, default=None)

    user = relationship('User', back_populates='shedule')

    def __str__(self) -> str:
        return f' #{self.user_id.name} {self.start_course }'
