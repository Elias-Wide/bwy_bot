from sqladmin import ModelView

from app.models.exercise import Course, Exercise, Shedule
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
    icon = 'fa-solid fa-user'


class ExerciseAdmin(ModelView, model=Exercise):
    column_list = [c.name for c in Exercise.__table__.c]
    icon = 'fa fa-file'


class CourseAdmin(ModelView, model=Course):
    column_list = [c.name for c in Course.__table__.c] + [
        Course.exercise,
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
