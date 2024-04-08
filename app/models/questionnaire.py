from typing import TypeVar

from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.db import Base

Self = TypeVar("Self", bound=None)


class Question(Base):
    text = Column(Text, nullable=False)
    possibleanswer_id = Column(Integer, ForeignKey('possibleanswer.id'))

    possibleanswer = relationship('PossibleAnswer', back_populates='question')

    def __str__(self: Self) -> str:
        return f' #{self.text}'


class PossibleAnswer(Base):
    text = Column(Text, nullable=False)

    question = relationship('Question', back_populates='possibleanswer')

    def __str__(self: Self) -> str:
        return f' #{self.text}'
