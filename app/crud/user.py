from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import relationship
from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
#    reservation = relationship('Reservation', back_populates='user')

    def __str__(self):
        return f' #{self.id}  {self.email}'
