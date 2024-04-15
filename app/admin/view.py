from sqladmin import ModelView

from app.models import (
    Course,
    Exercise,
    ExerciseWorkout,
    Schedule,
    Sleep,
    User,
    Workout,
    WorkoutCourse,
)


class UserAdmin(ModelView, model=User):
    name_plural = 'Пользователи'
    column_list = [User.id, User.email, User.gender] + [User.schedule]
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
    column_list = [Exercise.name, Exercise.descriptin, Exercise.video]
    column_details_list = [Exercise.name, Exercise.descriptin, Exercise.video]
    column_searchable_list = [Exercise.name, Exercise.video]
    icon = 'fa fa-file'


class ExerciseWorkoutAdmin(ModelView, model=ExerciseWorkout):
    name_plural = 'Упражнения в сете'
    column_list = [ExerciseWorkout.workout_id] + [
        ExerciseWorkout.workout,
        ExerciseWorkout.exercise,
    ]
    column_default_sort = 'workout_id'
    column_sortable_list = [
        ExerciseWorkout.workout_id,
        ExerciseWorkout.id,
    ]
    column_searchable_list = [WorkoutCourse.workout_id]
    icon = 'fa fa-file'


class WorkoutAdmin(ModelView, model=Workout):
    name_plural = 'Сеты'
    column_list = [Workout.name, Workout.descriptin, Workout.workout_type]
    icon = 'fa fa-file'
    column_default_sort = 'workout_type'
    column_searchable_list = [Workout.name, Workout.workout_type]
    icon = 'fa fa-file'


class WorkoutCourseAdmin(ModelView, model=WorkoutCourse):
    name_plural = 'Сеты в курсе тренировок'
    name_plural = 'Workout in course'
    column_list = [
        WorkoutCourse.course_id,
        WorkoutCourse.course_day,
        WorkoutCourse.am_noon_pm,
    ] + [
        WorkoutCourse.workout,
        WorkoutCourse.course,
    ]
    column_default_sort = 'course_day'
    column_sortable_list = [
        WorkoutCourse.course_id,
        WorkoutCourse.course_day,
    ]
    column_searchable_list = [
        WorkoutCourse.course_id,
    ]
    icon = 'fa fa-file'


class CourseAdmin(ModelView, model=Course):
    name_plural = 'Курс тренировок'
    column_exclude_list = [Course.id, Course.workout_course]
    column_searchable_list = [
        Course.name,
        Course.activity,
        Course.gender,
    ]
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
