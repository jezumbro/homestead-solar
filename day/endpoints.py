from datetime import date, datetime

from fastapi import APIRouter, Depends

from day.dependencies import get_by_date, get_solar_day_repository
from day.helpers import (
    convert_requests_to_time_values,
    group_by_localized_date,
    update_or_insert_requests,
)
from day.model import SolarDay
from day.repository import SolarDayRepository
from day.request_schema import CreateSolarDayRequest, SolarDayRequest
from day.response_schema import SolarDayResponse

router = APIRouter()


@router.post("/", response_model=SolarDayResponse)
def post_solar_day(
    req: CreateSolarDayRequest,
    repo: SolarDayRepository = Depends(get_solar_day_repository),
):
    sd = repo.find_one_by_date(req.date) or SolarDay(date=req.date)
    sd.weather = sd.weather or req.weather
    sd.upsert_values(convert_requests_to_time_values(req.values))
    repo.save(sd)
    return sd


@router.post("/values")
def insert_solar_days(
    reqs: list[SolarDayRequest],
    repo: SolarDayRepository = Depends(get_solar_day_repository),
):
    grouping = group_by_localized_date(reqs)
    existing_lookup = {x.date: x for x in repo.find_by_dates(grouping.keys())}
    docs = update_or_insert_requests(grouping, existing_lookup)
    result = repo.bulk_upsert(docs)
    return result.bulk_api_result


@router.get("/dates", response_model=list[date])
def get_unique_days(repo: SolarDayRepository = Depends(get_solar_day_repository)):
    return sorted(x.date for x in repo.find_by({}, projection={"date": 1}))


@router.get("/today", response_model=SolarDayResponse)
def get_data(repo: SolarDayRepository = Depends(get_solar_day_repository)):
    today = datetime.combine(datetime.today(), datetime.min.time())
    if sd := repo.find_one_by({"date": today}):
        return sd
    return SolarDayResponse(date=today)


@router.get("/{_date}", response_model=SolarDayResponse)
def get_data(sd: SolarDay = Depends(get_by_date)):
    return sd
