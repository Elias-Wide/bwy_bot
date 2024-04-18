from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.logging import get_logger
from app.crud.base import CRUDBase
from app.exceptions.workout import NoExerciseException, NoWorkoutsException
from app.models import User, Workout, WorkoutExercise

logger = get_logger(__name__)


class ExerciseCRUD(CRUDBase):

    @staticmethod
    async def get_groups(session: AsyncSession, user_id: int) -> list[Workout]:
        print(user_id)
        user = await session.scalars(
            select(User)
            .where(User.telegram_id == str(user_id))
        )
        user = user.first()
        groups = await session.scalars(
            select(Workout).where(
                and_(
                    Workout.gender == user.gender,
                    Workout.purpose == user.activity    #TODO: вроде добавили purpose - замени на ПР
                )
            )
        )
        groups = groups.all()
        if not groups:
            error_message = (
                f'В базе для "{user.gender}" и "{user.activity}" нет'
                 ' тренировок.'
            )
            logger.error(error_message)
            raise NoWorkoutsException(error_message)

        return groups

    @staticmethod
    async def get_exercises(
        session: AsyncSession,
        workout_id: int
    ) -> list[WorkoutExercise]:
        workout = await session.scalars(
            select(Workout)
            .where(Workout.id == workout_id)
            .options(
                selectinload(Workout.exercises)
                .joinedload(WorkoutExercise.exercise)
            )
        )
        workout = workout.first()
        exercises = list(workout.exercises)
        if not exercises:
            error_message = (
                f'В WorkoutExercise для {workout.name} не назначены'
                 ' упражнения.'
            )
            logger.error(error_message)
            raise NoExerciseException(error_message)
        return exercises


workout_crud = ExerciseCRUD(Workout)
