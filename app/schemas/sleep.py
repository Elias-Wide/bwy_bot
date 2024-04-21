from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SleepDB(BaseModel):
    id: int
    go_to_bed_time: Optional[datetime]
    wake_up_time: Optional[datetime]
    sleep_duration: Optional[float]
    user_id: int

    class Config:
        orm_mode = True
