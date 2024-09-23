"""Модуль конфигурации adminpages."""

from typing import Any, TypeAlias

from sqladmin import ModelView
from starlette.requests import Request

from app.core.constants import (
    ACTIVITY_PURPOSE,
    GENDER,
    PLURAL_NAME_ADVERTISEMENT,
    PLURAL_NAME_CALORIE,
    PLURAL_NAME_EXERCISE,
    PLURAL_NAME_SCHEDULE,
    PLURAL_NAME_SLEEP,
    PLURAL_NAME_USER,
    PLURAL_NAME_WORKOUT,
    PLURAL_NAME_WORKOUT_EXERCISE,
    WORKOUT_TYPE,
)
from app.core.logging import get_logger
from app.crud.workout import workout_crud
from app.models import (
    Advertisement,
    Calorie,
    Exercise,
    Schedule,
    Sleep,
    User,
    Workout,
    WorkoutExercise,
)
from app.validators.admin_view_validators import (
    validate_upload_image,
    validate_upload_video,
)

MyAny: TypeAlias = Any
logger = get_logger(__name__)


class UserAdmin(ModelView, model=User):
    """Настройка страницы пользователей."""

    name_plural = PLURAL_NAME_USER
    column_list = [User.id, User.email, User.gender, User.schedule]
    column_details_exclude_list = [
        User.hashed_password,
        User.gender,
        User.sleep,
    ]
    can_delete = False
    column_searchable_list = [User.email, User.telegram_id, User.name]
    icon = 'fa-solid fa-user'


class ExerciseAdmin(ModelView, model=Exercise):
    """Настройка страницы упражнений."""

    page_size = 25
    name_plural = PLURAL_NAME_EXERCISE
    column_list = [Exercise.name, Exercise.description, Exercise.video]
    column_details_list = [Exercise.name, Exercise.description, Exercise.video]
    column_searchable_list = [Exercise.name, Exercise.video]
    icon = 'fa fa-file'

    async def on_model_change(
        self,
        data: dict,
        model: MyAny,
        is_created: bool,
        request: Request,
    ) -> None:
        """Валидация загружаемого видео."""
        await validate_upload_video(data)


class WorkoutExerciseAdmin(ModelView, model=WorkoutExercise):
    """Настройка страницы связи упражнений с тренировками."""

    page_size = 25
    name_plural = PLURAL_NAME_WORKOUT_EXERCISE
    column_list = [
        WorkoutExercise.workout_id,
        WorkoutExercise.workout,
        WorkoutExercise.exercise,
        WorkoutExercise.sequence_number,
    ]
    column_default_sort = 'workout_id'
    column_sortable_list = [
        WorkoutExercise.workout_id,
        WorkoutExercise.sequence_number,
    ]
    column_searchable_list = [WorkoutExercise.workout_id]
    icon = 'fa fa-file'


class WorkoutAdmin(ModelView, model=Workout):
    """Настройка страницы упражнений связанных с гендер-цель."""

    page_size = 25
    name_plural = PLURAL_NAME_WORKOUT
    column_list = [Workout.name, Workout.group]
    icon = 'fa fa-file'
    column_default_sort = 'group'
    column_searchable_list = [Workout.name, Workout.group]
    icon = 'fa fa-file'

    async def on_model_change(
        self,
        data: dict,
        model: MyAny,
        is_created: bool,
        request: Request,
    ) -> None:
        """Автозаполнение имени упражнения."""
        if is_created:
            set_count = await workout_crud.get_set_count(data)
            data['name'] = (
                f'{set_count}. '
                f'{dict(WORKOUT_TYPE)[data["group"]]}'
                f'-{dict(GENDER)[data["gender"]]}'
                f'-{dict(ACTIVITY_PURPOSE)[data["purpose"]]}'
            )


class ScheduleAdmin(ModelView, model=Schedule):
    """Настройка страницы управления напоминаниями."""

    name_plural = PLURAL_NAME_SCHEDULE
    column_list = [c.name for c in Schedule.__table__.c] + [
        Schedule.user,
    ]
    column_searchable_list = [
        Schedule.user_id,
    ]
    icon = 'fa fa-file'


class SleepAdmin(ModelView, model=Sleep):
    """Настройка страницы статистики сна."""

    name_plural = PLURAL_NAME_SLEEP
    column_list = [c.name for c in Sleep.__table__.c] + [
        Sleep.user,
    ]
    icon = 'fa fa-file'


class CalorieAdmin(ModelView, model=Calorie):
    """Настройка статистики управления картинками КБЖУ."""

    name_plural = PLURAL_NAME_CALORIE
    column_list = [c.name for c in Calorie.__table__.c]
    icon = 'fa fa-file'

    async def on_model_change(
        self,
        data: dict,
        model: MyAny,
        is_created: bool,
        request: Request,
    ) -> None:
        """Валидация загружаемой картинки."""
        if data['picture'].size is not None:
            await validate_upload_image(data['picture'])


class AdvertisementAdmin(ModelView, model=Advertisement):
    """Настройка страницы управления ракламными анонсами."""

    name_plural = PLURAL_NAME_ADVERTISEMENT
    column_list = [c.name for c in Advertisement.__table__.c]
    column_searchable_list = [
        Advertisement.hour_to_adv,
        Advertisement.active,
        Advertisement.gender,
    ]
    column_sortable_list = [Advertisement.active, Advertisement.hour_to_adv]
    icon = 'fa fa-book'

    async def on_model_change(
        self,
        data: dict,
        model: MyAny,
        is_created: bool,
        request: Request,
    ) -> None:
        """Валидация загружаемой картинки."""
        if data['image'].size is not None:
            await validate_upload_image(data['image'])
