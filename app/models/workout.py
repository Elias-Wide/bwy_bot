"""Модуль содержащий классы моделей тренировок."""

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ChoiceType

from app.core.config import UPLOAD_DIR
from app.core.constants import ACTIVITY_PURPOSE, GENDER, WORKOUT_TYPE
from app.core.db import Base

storage = FileSystemStorage(path=UPLOAD_DIR)


class Exercise(Base):
    """Класс, описывающий модель упражнений В БД."""

    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    description: Mapped[str]
    video: Mapped[FileType] = mapped_column(FileType(storage=storage))
    workouts: Mapped[list['WorkoutExercise']] = relationship(
        back_populates='exercise',
    )

    def __str__(self) -> str:
        """Строковое представление экземпляра класса."""
        return f'{self.name}'


class Workout(Base):
    """Класс, описывающий модель тренировок В БД.

    Объект тренировки содержит в себе объекты упражнений,
    зависимость через вспомогательную модель WorkoutExercise.
    """

    name: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
        default='Name will be autofilled',
    )
    group: Mapped[ChoiceType] = mapped_column(ChoiceType(WORKOUT_TYPE))
    gender: Mapped[ChoiceType] = mapped_column(ChoiceType(GENDER))
    purpose: Mapped[ChoiceType] = mapped_column(ChoiceType(ACTIVITY_PURPOSE))
    exercises: Mapped[list['WorkoutExercise']] = relationship(
        back_populates='workout',
    )

    def __str__(self) -> str:
        """Строковое представление экземпляра класса."""
        return f'{self.name}'


class WorkoutExercise(Base):
    """
    Вспомогательная модель для связи таблиц.

    Устанавливает зависимость между таблицами Workout и Exercise.
    """

    exercise_id: Mapped[int] = mapped_column(
        ForeignKey('exercise.id', ondelete='CASCADE'),
        nullable=False,
    )
    workout_id: Mapped[int] = mapped_column(
        ForeignKey('workout.id', ondelete='CASCADE'),
        nullable=False,
    )
    sequence_number: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        default=1,
    )
    workout: Mapped['Workout'] = relationship(back_populates='exercises')
    exercise: Mapped['Exercise'] = relationship(back_populates='workouts')

    def __str__(self) -> str:
        """Строковое представление экземпляра класса."""
        return f'workout:{self.workout_id} - exercise:{self.exercise_id}'
