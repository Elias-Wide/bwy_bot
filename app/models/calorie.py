from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import Column
from sqlalchemy_utils import ChoiceType

from app.core.config import STATIC_DIR
from app.core.constants import ACTIVITY_PURPOSE, GENDER
from app.core.db import Base

storage = FileSystemStorage(path=STATIC_DIR)


class Calorie(Base):
    gender = Column(ChoiceType(GENDER))
    activity_purpose = Column(ChoiceType(ACTIVITY_PURPOSE))
    picture = Column(FileType(storage=storage))

    def __str__(self) -> str:
        return f' Калории для {self.gender} - {self.activity }'
