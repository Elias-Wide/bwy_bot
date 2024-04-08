from typing import Optional, Text

from pydantic import BaseModel


class Question(BaseModel):
    text: Optional[Text]
    possible_answer_id: int

    class Config:
        orm_mode = True


class PossibleAnswer(BaseModel):
    text: Optional[Text]
