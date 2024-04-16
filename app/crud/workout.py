from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.workout import Exercise, Workout



class ExerciseCRUD(CRUDBase):

    @staticmethod
    async def get_exercises(session: AsyncSession, workout_id: int) -> list[Exercise]:
        exercises = await session.scalars(
            select(Exercise).where(Exercise.workout_id == workout_id)
        )
        return exercises.all()


workout_crud = ExerciseCRUD(Workout)
