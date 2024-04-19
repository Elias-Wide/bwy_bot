from app.crud.base import CRUDBase
from app.models import User, Schedule

user_crud = CRUDBase(Schedule)
