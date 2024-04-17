from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Exercise, User, Workout



class ExerciseCRUD(CRUDBase):

    @staticmethod
    async def get_groups(session: AsyncSession, user_id: int) -> list[Workout]:
        print(user_id)
        user = await session.scalars(
            select(User)
            .where(User.telegram_id == str(user_id))
        )
        user = user.first()
        print(user)
        groups = await session.scalars(
            select(Workout).where(
                and_(
                    Workout.gender == user.gender,
                    Workout.purpose == user.activity    #TODO: вроде добавили purpose - замени на ПР
                )
            )
        )
        return groups.all()

    @staticmethod
    async def get_exercises(
        session: AsyncSession,
        workout_id: int
    ) -> list[Exercise]:
        exercises = await session.scalars(
            select(Exercise).where(Exercise.workout_id == workout_id)
        )
        return exercises.all()


workout_crud = ExerciseCRUD(Workout)
