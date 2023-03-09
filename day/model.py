from datetime import datetime

from database import MongoModel
from pydantic import BaseModel, Field


class TimeValues(BaseModel):
    end_date: datetime
    start_date: datetime
    value: float


class SolarDay(MongoModel):
    date: datetime
    values: list[TimeValues] = Field(default_factory=list)
