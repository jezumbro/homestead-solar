from datetime import datetime

from fastapi import APIRouter, Depends

from day.dependencies import get_solar_day_repository
from day.repository import SolarDayRepository
from day.response_schema import SolarDayResponse

router = APIRouter()


@router.get("/today", response_model=SolarDayResponse)
def get_data(repo: SolarDayRepository = Depends(get_solar_day_repository)):
    today = datetime.combine(datetime.today(), datetime.min.time())
    if sd := repo.find_one_by({"date": today}):
        return sd
    return SolarDayResponse(date=today)
