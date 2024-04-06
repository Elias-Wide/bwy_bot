from sqladmin import ModelView

from app.models.file import File
from app.models.user import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    icon = 'fa-solid fa-user'


class FileAdmin(ModelView, model=File):
    column_list = [File.id, File.file]
    icon = 'fa fa-file'
