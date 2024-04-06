from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from typing import TypeVar


from app.core.db import Base

Self = TypeVar("Self", bound="User")


class User(SQLAlchemyBaseUserTable[int], Base):

    def __str__(self: Self) -> str:
        return f' #{self.id}  {self.email}'
