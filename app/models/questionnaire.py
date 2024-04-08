from app.core.config import Self

from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


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
