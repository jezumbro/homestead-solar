from datetime import date, datetime

from database import MongoModel
from pydantic import BaseModel, Field, validator
from util import add_utc


class TimeValueResponse(BaseModel):
    end_date: datetime
    start_date: datetime
    value: float

    _utc_convert = validator("start_date", "end_date", allow_reuse=True)(add_utc)


class SolarDayResponse(MongoModel):
    date: date
    values: list[TimeValueResponse] = Field(default_factory=list)
