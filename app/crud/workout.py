from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.logging import get_logger
from app.crud.base import CRUDBase
from app.exceptions.workout import NoExerciseException, NoWorkoutsException
from app.models import User, Workout, WorkoutExercise

logger = get_logger(__name__)


class ExerciseCRUD(CRUDBase):

    @staticmethod
    async def get_groups(session: AsyncSession, user: User) -> list[Workout]:
        groups = await session.scalars(
            select(Workout).where(
                and_(
                    Workout.gender == user.gender,
                    Workout.purpose == user.purpose,
                ),
            ),
        )
        groups = groups.all()
        if not groups:
            logger.error(
                'В базе для %s и %s нет тренировок.',
                user.gender,
                user.purpose,
            )
            raise NoWorkoutsException()

        return groups

    @staticmethod
    async def get_exercises(
        session: AsyncSession,
        workout_id: int,
    ) -> list[WorkoutExercise]:
        workout = await session.scalars(
            select(Workout)
            .where(Workout.id == workout_id)
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


workout_crud = ExerciseCRUD(Workout)
