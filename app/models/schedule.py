from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.db import Base


class Schedule(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    start_course = Column(DateTime, default=None)
    stop_reminder_train = Column(Boolean, default=True)
    stop_reminder_sleep = Column(Boolean, default=True)
    stop_reminder_calories = Column(Boolean, default=True)

    user = relationship('User', back_populates='schedule', uselist=False)

    def __str__(self) -> str:
        return (
            f'Пользователь с id {self.user_id} начал курс {self.start_course }'
        )