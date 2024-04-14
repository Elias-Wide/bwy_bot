from sqladmin import ModelView

from app.models.exercise import (
    Course,
    Exercise,
    ExerciseWorkout,
    Shedule,
    Workout,
    WorkoutCourse,
)
from app.models.questionnaire import PossibleAnswer, Question
from app.models.sleep import Sleep
from app.models.user import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.gender]
    column_details_exclude_list = [
        User.hashed_password,
        User.gender,
        User.sleep,
    ]
    can_delete = False
    column_searchable_list = [User.email, User.telegram_id, User.name]
    icon = 'fa-solid fa-user'


class ExerciseAdmin(ModelView, model=Exercise):
    column_list = [Exercise.name, Exercise.descriptin, Exercise.video]
    column_details_list = [Exercise.name, Exercise.descriptin, Exercise.video]
    column_searchable_list = [Exercise.name, Exercise.video]
    icon = 'fa fa-file'


class ExerciseWorkoutAdmin(ModelView, model=ExerciseWorkout):
    name_plural = 'Exercise in  workout'
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
    column_list = [Workout.name, Workout.descriptin, Workout.workout_type]
    icon = 'fa fa-file'
    column_default_sort = 'workout_type'
    column_searchable_list = [Workout.name, Workout.workout_type]
    icon = 'fa fa-file'


class WorkoutCourseAdmin(ModelView, model=WorkoutCourse):
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
    column_exclude_list = [Course.id, Course.workout_course]
    column_searchable_list = [
        Course.name,
        Course.activity,
        Course.gender,
    ]
    icon = 'fa fa-file'


class SheduleAdmin(ModelView, model=Shedule):
    column_list = [c.name for c in Shedule.__table__.c] + [
        Shedule.user,
    ]
    icon = 'fa fa-file'


class QuestionAdmin(ModelView, model=Question):
    column_list = [c.name for c in Question.__table__.c] + [
        Question.possibleanswer,
    ]
    icon = 'fa fa-book'


class AnswerAdmin(ModelView, model=PossibleAnswer):
    column_list = [c.name for c in PossibleAnswer.__table__.c] + [
        PossibleAnswer.question,
    ]
    icon = 'fa fa-book'


class SleepAdmin(ModelView, model=Sleep):
    column_list = [c.name for c in Sleep.__table__.c] + [
        Sleep.user,
    ]
    icon = 'fa fa-book'
