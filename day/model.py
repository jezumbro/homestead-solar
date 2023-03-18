from datetime import datetime
from typing import Iterable, Optional

from database import MongoModel
from loguru import logger
from pydantic import BaseModel, Field, validator
from util import no_timezone_information


class TimeValue(BaseModel):
    end_date: datetime
    start_date: datetime
    value: float

    _no_tz_info = validator("start_date", "end_date", allow_reuse=True)(
        no_timezone_information
    )


class Temperature(BaseModel):
    min: int
    max: int


class Weather(BaseModel):
    code: str
    display: str
    temperature: Temperature


class SolarDay(MongoModel):
    date: datetime
    values: list[TimeValue] = Field(default_factory=list)
    weather: Optional[Weather] = Field(None)

    def existing_lookup(self) -> dict[datetime, TimeValue]:
        return {x.start_date: x for x in self.values}

    def upsert_weather(self, weather: Optional[Weather]):
        if not weather:
            return
        self.weather = weather

    @staticmethod
    def by_start_date(value: TimeValue):
        return value.start_date

    def sort_values(self):
        self.values.sort(key=self.by_start_date)

    def upsert_values(self, values: Iterable[TimeValue]):
        lookup = self.existing_lookup()
        seen = set()
        for value in values:
            start_date = value.start_date
            if start_date in seen:
                logger.warning(
                    f"attempted to insert {start_date} when it already existed"
                )
                continue
            seen.add(start_date)
            if existing := lookup.get(start_date):
                existing.value = value.value
                continue
            self.values.append(value)
        self.sort_values()
