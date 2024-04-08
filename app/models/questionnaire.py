from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Question:
    text = Column(Text, nullable=False)
    possible_answer_id = Column(
        Integer,
        ForeignKey(
            'possible_answer.id',
            name='fk_question_possible_answer_id_possible_answer',
        ),
    )

    possible_answer_id = relationship(
        'Possible_answer_id', back_populates='question')


class PossibleAnswer:
    text = Column(Text, nullable=False)
