from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import Column

from app.core.db import Base

storage = FileSystemStorage(path='./upload')


class File(Base):

    file = Column(FileType(storage=storage))
