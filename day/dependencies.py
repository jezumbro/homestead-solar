from datetime import date

from database import get_database
from fastapi import Depends, HTTPException

from day.model import SolarDay
from day.repository import SolarDayRepository


def get_solar_day_repository(database=Depends(get_database)) -> SolarDayRepository:
    return SolarDayRepository(database)


def get_by_date(
    _date: date, repo: SolarDayRepository = Depends(get_solar_day_repository)
) -> SolarDay:
    if sd := repo.find_one_by_date(_date):
        return sd
    raise HTTPException(404, f"Unable to find matching data for date={_date}")
