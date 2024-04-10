from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):

    def __str__(self) -> str:
        return f' #{self.id}  {self.email}'
