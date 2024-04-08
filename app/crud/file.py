from sqlalchemy import Column
from app.core.db import Base
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType

storage = FileSystemStorage(path="./upload")


class File(Base):

    file = Column(FileType(storage=storage))
