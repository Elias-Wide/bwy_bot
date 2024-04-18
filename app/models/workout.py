from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy_utils import ChoiceType

from app.core.config import UPLOAD_DIR
from app.core.constants import (
    ACTIVITY_PURPOSE,
    WORKOUT_TYPE,
    GENDER,
)
from app.core.db import Base

storage = FileSystemStorage(path=UPLOAD_DIR)


class Exercise(Base):

    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    description: Mapped[str]
    video: Mapped[FileType] = mapped_column(FileType(storage=storage))
    workouts: Mapped[list['WorkoutExercise']] = relationship(
        back_populates='exercise'
    )

    def __str__(self) -> str:
        return f'{self.name}'


class Workout(Base):

    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    group: Mapped[ChoiceType] = mapped_column(ChoiceType(WORKOUT_TYPE))
    gender: Mapped[ChoiceType] = mapped_column(ChoiceType(GENDER))
    purpose: Mapped[ChoiceType] = mapped_column(ChoiceType(ACTIVITY_PURPOSE))
    exercises: Mapped[list['WorkoutExercise']] = relationship(
        back_populates='workout'
    )

    def __str__(self) -> str:
        return f'{self.name}'


class WorkoutExercise(Base):
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey('exercise.id', ondelete='CASCADE'),
        nullable=False
    )
    workout_id: Mapped[int] = mapped_column(
        ForeignKey('workout.id', ondelete='CASCADE'),
        nullable=False
    )
    workout: Mapped['Workout'] = relationship(back_populates='exercises')
    exercise: Mapped['Exercise'] = relationship(back_populates='workouts')


    def __str__(self) -> str:
        return f'''workout:{self.workout_id.__str__} - exercise:{self.exercise_id}'''
