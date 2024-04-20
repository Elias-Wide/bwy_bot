from sqladmin import ModelView

from app.models import (
    Calorie,
    Exercise,
    Schedule,
    Sleep,
    User,
    Workout,
    WorkoutExercise,
)


class UserAdmin(ModelView, model=User):
    name_plural = 'Пользователи'
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
    name_plural = 'Упражнения'
    column_list = [Exercise.name, Exercise.description, Exercise.video]
    column_details_list = [Exercise.name, Exercise.description, Exercise.video]
    column_searchable_list = [Exercise.name, Exercise.video]
    icon = 'fa fa-file'


class WorkoutExerciseAdmin(ModelView, model=WorkoutExercise):
    name_plural = 'Упражнения в тренировках'
    column_list = [
        WorkoutExercise.workout_id,
        WorkoutExercise.workout,
        WorkoutExercise.exercise,
    ]
    column_default_sort = 'workout_id'
    column_sortable_list = [
        WorkoutExercise.workout_id,
        WorkoutExercise.id,
    ]
    column_searchable_list = [WorkoutExercise.workout_id]
    icon = 'fa fa-file'


class WorkoutAdmin(ModelView, model=Workout):

    name_plural = 'Тренировки'
    column_list = [Workout.name, Workout.group]
    icon = 'fa fa-file'
    column_default_sort = 'group'
    column_searchable_list = [Workout.name, Workout.group]
    icon = 'fa fa-file'


class ScheduleAdmin(ModelView, model=Schedule):
    name_plural = 'Напоминания'
    column_list = [c.name for c in Schedule.__table__.c] + [
        Schedule.user,
    ]
    icon = 'fa fa-file'


class SleepAdmin(ModelView, model=Sleep):
    name_plural = 'Сон'
    column_list = [c.name for c in Sleep.__table__.c] + [
        Sleep.user,
    ]
    icon = 'fa fa-book'


class CalorieAdmin(ModelView, model=Calorie):
    name_plural = 'Калории(картинки в static)'
    column_list = [c.name for c in Calorie.__table__.c]
    icon = 'fa fa-file'
