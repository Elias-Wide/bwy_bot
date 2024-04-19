from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.db import Base


class Schedule(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    start_course = Column(DateTime, default=datetime.now)
    stop_reminder_train = Column(Boolean, default=False)
    stop_reminder_sleep = Column(Boolean, default=False)
    stop_reminder_calories = Column(Boolean, default=False)

    user = relationship('User', back_populates='schedule', uselist=False)

    def __str__(self) -> str:
        return (
            f'Пользователь с id {self.user_id} начал курс {self.start_course }'
        )
