from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import Column
from sqlalchemy_utils import ChoiceType

from app.core.db import Base
from app.core.constants import WORKOUT_TYPE

storage = FileSystemStorage(path='./upload')


class File(Base):

    workout_type = Column(ChoiceType(WORKOUT_TYPE))
    file = Column(FileType(storage=storage))
