from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.config import Self
from app.core.db import Base


class Sleep(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    go_to_bed_time = Column(DateTime, default=None)
    wake_up_time = Column(DateTime, default=None)
    sleep_duration = Column(DateTime, default=None)

    user = relationship('User', back_populates='sleep')

    def __str__(self: Self) -> str:
        return f'#{self.id}: {self.sleep_duration}'
