from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, root_validator, validator
from util import has_timezone_information, to_localized_date

from day.model import Weather


class SolarDayRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    value: Optional[float] = None

    _validate_dt = validator("start_date", "end_date", allow_reuse=True)(
        has_timezone_information
    )


class CreateSolarDayRequest(BaseModel):
    date: date
    values: list[SolarDayRequest] = Field(default_factory=list)
    weather: Optional[Weather]

    @root_validator
    def _validate_values_in_date(cls, values):
        dates = set((to_localized_date(x.start_date) for x in values["values"]))
        d = {values["date"]}
        if dates - d:
            raise ValueError("Values must match the same localized date")
        return values
