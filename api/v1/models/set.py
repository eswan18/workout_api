from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class SetIn(BaseModel):
    start_time: datetime
    weight: float
    weight_unit: str | None
    reps: int | None
    seconds: int | None
    notes: str
    # Relations
    exercise_id: UUID
    workout_id: UUID


class SetInDB(SetIn):
    id: UUID
    user_id: UUID

    class Config:
        orm_mode = True
