from sqladmin import ModelView

from app.models.file import File
from app.models.questionnaire import PossibleAnswer, Question
from app.models.user import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.gender]
    # column_list = [
    #     c.name for c in User.__table__.c]
    column_details_exclude_list = [User.hashed_password, User.gender]
    can_delete = False
    icon = 'fa-solid fa-user'


class FileAdmin(ModelView, model=File):
    column_list = [File.id, File.workout_type, File.file]
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
