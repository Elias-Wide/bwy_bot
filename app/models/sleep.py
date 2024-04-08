from app.core.config import Self

from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from app.core.db import Base

class Sleep(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    go_to_bed_time = Column(DateTime, default=None)
    wake_up_time = Column(DateTime, default=None)
    sleep_duration = Column(DateTime, default=None)

    def __str__(self: Self) -> str:
        return (
            f'#{self.id}: с {self.go_to_bed_time} 
            по {self.wake_up_time} = {self.sleep_duration}'
        )
            