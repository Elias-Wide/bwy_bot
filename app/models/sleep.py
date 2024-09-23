"""Классы, описывающие модели логики сна."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.db import Base


class Sleep(Base):
    """Класс записи сна.

    Args:
        user_id: id пользователя
        go_to_bed_time: время отхода ко сну
        wake_up_time: продолжительность сна
        sleep_duration: продолжительность сна
    """

    user_id = Column(Integer, ForeignKey('user.id'))
    go_to_bed_time = Column(DateTime, default=datetime.now)
    wake_up_time = Column(DateTime, nullable=True)
    sleep_duration = Column(Float, default=8)

    user = relationship('User', back_populates='sleep')

    def __str__(self) -> str:
        """Строковое представление экземпляра класса."""
        return f'{self.id}: {self.sleep_duration}'
