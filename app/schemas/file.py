from typing import Optional

from pydantic import BaseModel


class File(BaseModel):
    file: Optional[str]

    class Config:
        orm_mode = True
