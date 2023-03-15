from datetime import date, datetime

from fastapi import APIRouter, Depends

from day.dependencies import get_solar_day_repository
from day.helpers import group_by_localized_date, update_or_insert_requests
from day.repository import SolarDayRepository
from day.request_schema import SolarDayRequest
from day.response_schema import SolarDayResponse

router = APIRouter()


@router.post("/")
def insert_solar_days(
    reqs: list[SolarDayRequest],
    repo: SolarDayRepository = Depends(get_solar_day_repository),
):
    grouping = group_by_localized_date(reqs)
    existing_lookup = {x.date: x for x in repo.find_by_dates(grouping.keys())}
    docs = update_or_insert_requests(grouping, existing_lookup)
    result = repo.bulk_upsert(docs)
    return {"inserted": result.inserted_count, "updated": result.upserted_count}


@router.get("/dates", response_model=list[date])
def get_unique_days(repo: SolarDayRepository = Depends(get_solar_day_repository)):
    return sorted(x.date for x in repo.find_by({}, projection={"date": 1}))


@router.get("/dates/{_date}", response_model=SolarDayResponse)
def get_data(_date: date, repo: SolarDayRepository = Depends(get_solar_day_repository)):
    dt = datetime.combine(_date, datetime.min.time())
    if sd := repo.find_one_by({"date": dt}):
        return sd
    return SolarDayResponse(date=dt)


@router.get("/today", response_model=SolarDayResponse)
def get_data(repo: SolarDayRepository = Depends(get_solar_day_repository)):
    today = datetime.combine(datetime.today(), datetime.min.time())
    if sd := repo.find_one_by({"date": today}):
        return sd
    return SolarDayResponse(date=today)
