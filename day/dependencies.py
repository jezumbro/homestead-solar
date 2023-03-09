from database import get_database
from fastapi import Depends

from day.repository import SolarDayRepository


def get_solar_day_repository(database=Depends(get_database)) -> SolarDayRepository:
    return SolarDayRepository(database)
