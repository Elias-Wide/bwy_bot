from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.constants import SLEEP
from app.core.db import Base


class Sleep(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    go_to_bed_time = Column(DateTime, default=datetime.now)
    wake_up_time = Column(DateTime, default=datetime.now)
    sleep_duration = Column(Float, default=8)

    user = relationship('User', back_populates=SLEEP)

    def __str__(self) -> str:
        return f'{self.id}: {self.sleep_duration}'
