from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from app.core.config import UPLOAD_DIR
from app.core.constants import (
    ACTIVITY_PURPOSE,
    AM_NOON_PM,
    GENDER,
    WORKOUT_TYPE,
)
from app.core.db import Base

storage = FileSystemStorage(path=UPLOAD_DIR)


class Exercise(Base):
    __tablename__ = 'exercise'
    name = Column(String(255), unique=True, nullable=False)
    descriptin = Column(Text)
    video = Column(FileType(storage=storage))
    exercise_workout = relationship(
        'ExerciseWorkout',
        back_populates='exercise',
    )

    def __str__(self) -> str:
        return f'{self.name}'


class Workout(Base):
    __tablename__ = 'workout'
    name = Column(String(255), unique=True, nullable=False)
    descriptin = Column(Text)
    workout_type = Column(ChoiceType(WORKOUT_TYPE))

    exercise_workout = relationship(
        'ExerciseWorkout',
        back_populates='workout',
    )
    workout_course = relationship('WorkoutCourse', back_populates='workout')

    def __str__(self) -> str:
        return f'{self.name}'


class ExerciseWorkout(Base):
    __tablename__ = 'exercise_workout'
    exercise_id = Column(Integer(), ForeignKey('exercise.id'))
    workout_id = Column(Integer(), ForeignKey('workout.id'))
    sequence_number = Column(String(100))
    descriptin = Column(Text)
    workout = relationship('Workout', back_populates='exercise_workout')
    exercise = relationship('Exercise', back_populates='exercise_workout')

    def __str__(self) -> str:
        return f'''{self.sequence_number} -
                workout:{self.workout_id} -
                exercise:{self.exercise_id}'''


class Course(Base):
    name = Column(String(255), unique=True, nullable=False)
    descriptin = Column(Text)
    gender = Column(ChoiceType(GENDER))
    activity = Column(ChoiceType(ACTIVITY_PURPOSE))
    workout_course = relationship('WorkoutCourse', back_populates='course')

    def __str__(self) -> str:
        return f'{self.gender} + {self.activity}'


class WorkoutCourse(Base):
    __tablename__ = 'workout_course'
    course_id = Column(Integer(), ForeignKey('course.id'))
    workout_id = Column(Integer(), ForeignKey('workout.id'))
    course_day = Column(Integer())
    am_noon_pm = Column(ChoiceType(AM_NOON_PM))
    descriptin = Column(Text)
    workout = relationship('Workout', back_populates='workout_course')
    course = relationship('Course', back_populates='workout_course')

    def __str__(self) -> str:
        return f'''{self.course_day} -
                course:{self.course_id} -
                workout:{self.workout_id}'''
