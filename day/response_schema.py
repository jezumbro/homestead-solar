from datetime import date, datetime
from typing import Optional

from database import MongoModel
from pydantic import BaseModel, Field, validator
from util import add_utc


class TimeValueResponse(BaseModel):
    class Config:
        orm_mode = True

    end_date: datetime
    start_date: datetime
    value: float

    _utc_convert = validator("start_date", "end_date", allow_reuse=True)(add_utc)


class TemperatureResponse(BaseModel):
    class Config:
        orm_mode = True

    min: int
    max: int


class WeatherResponse(BaseModel):
    class Config:
        orm_mode = True

    code: str
    display: str
    temperature: TemperatureResponse


class SunriseSunsetResponse(BaseModel):
    sunrise: datetime
    sunset: datetime

    _utc_convert = validator("sunrise", "sunset", allow_reuse=True)(add_utc)


class TimesResponse(BaseModel):
    solar_noon: datetime
    local: SunriseSunsetResponse
    civil: SunriseSunsetResponse
    nautical: SunriseSunsetResponse
    astronomical: SunriseSunsetResponse

    _utc_convert = validator("solar_noon", allow_reuse=True)(add_utc)


class SolarDayResponse(MongoModel):
    date: date
    values: list[TimeValueResponse] = Field(default_factory=list)
    weather: Optional[WeatherResponse]
    times: Optional[TimesResponse]
