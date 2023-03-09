from datetime import date

from database import MongoModel
from pydantic import Field

from day.model import TimeValues


class SolarDayResponse(MongoModel):
    date: date
    values: list[TimeValues] = Field(default_factory=list)
