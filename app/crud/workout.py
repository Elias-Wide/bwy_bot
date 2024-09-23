"""CRUD операции относящийся к участку тренировок."""

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.constants import WORKOUT_CRUD_ERROR
from app.core.db import AsyncSessionLocal
from app.core.logging import get_logger
from app.crud.base import CRUDBase
from app.exceptions.workout import NoExerciseException, NoWorkoutsException
from app.models import User, Workout, WorkoutExercise

logger = get_logger(__name__)


class ExerciseCRUD(CRUDBase):
    """Класс CRUD операций относящийся к участку тренировок."""

    @staticmethod
    async def get_workouts_by_group(
        session: AsyncSession,
        workout_group: str,
        user: User,
    ) -> list[Workout]:
        """Запрос в БД для получения списка тренировок.

        Передается имя запращиваемой группы тренировок,
        возвращает список объектов тренировок.
        """
        workouts = await session.scalars(
            select(Workout).where(
                and_(
                    Workout.gender == user.gender,
                    Workout.purpose == user.purpose,
                    Workout.group == workout_group,
                ),
            ),
        )
        workouts = workouts.all()
        if not workouts:
            logger.error(
                WORKOUT_CRUD_ERROR,
                user.gender,
                user.purpose,
                workout_group,
            )
            raise NoWorkoutsException()
        return workouts

    @staticmethod
    async def get_exercises(
        session: AsyncSession,
        workout_id: int,
        page: int,
    ) -> list[WorkoutExercise]:
        """Запрос в БД для получения упражнений по переданному workout id."""
        workout = await session.scalars(
            select(Workout, WorkoutExercise.sequence_number)
            .where(Workout.id == workout_id)
            .order_by(WorkoutExercise.sequence_number)
            .options(
                selectinload(Workout.exercises).joinedload(
                    WorkoutExercise.exercise,
                ),
            ),
        )
        workout = workout.first()
        exercises = list(workout.exercises)
        if not exercises:
            logger.error('Нет упражнений для %s.', workout.name)
            raise NoExerciseException()
        return exercises

    @staticmethod
    async def get_random_workout_id(
        session: AsyncSession,
        user: User,
        workout_group: str,
    ) -> int:
        """Запрос в БД для получения рандомного workout id.

        Функция получает объект пользователя и имя группы тренировок,
        id тренировки выбирается рандомно.
        """
        result = await session.scalars(
            select(Workout)
            .where(
                and_(
                    Workout.gender == user.gender,
                    Workout.purpose == user.purpose,
                    Workout.group == workout_group,
                ),
            )
            .order_by(func.random()),
        )
        random_workout = result.first()
        if not random_workout:
            raise NoExerciseException()
        return random_workout.id

    @staticmethod
    async def get_set_count(data: dict) -> str:
        """Запрос в БД для получения количества тренировок с параметрами.

        Возвращает количество тренировок с одинаковыми параметрами
        группа мышц, гендер, цель, для. Для формирования

        """
        async with AsyncSessionLocal() as session:
            set_count = await session.scalar(
                select(func.count(Workout.id)).where(
                    and_(
                        Workout.gender == data['gender'],
                        Workout.purpose == data['purpose'],
                        Workout.group == data['group'],
                    ),
                ),
            )
        return str(int(set_count) + 1)


workout_crud = ExerciseCRUD(Workout)
