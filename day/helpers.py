from datetime import date, datetime
from typing import Iterable

from dateutil import tz
from more_itertools import map_reduce

from day.model import SolarDay, TimeValue
from day.request_schema import SolarDayRequest


def by_localized_date(req: SolarDayRequest) -> date:
    return req.start_date.astimezone(tz.gettz("America/Chicago")).date()


def group_by_localized_date(
    reqs: list[SolarDayRequest],
) -> dict[date, list[SolarDayRequest]]:
    return map_reduce(reqs, keyfunc=by_localized_date)


def convert_requests_to_time_values(reqs: list[SolarDayRequest]) -> Iterable[TimeValue]:
    for req in reqs:
        yield TimeValue(
            start_date=req.start_date.replace(tzinfo=None),
            end_date=req.end_date.replace(tzinfo=None),
            value=req.value,
        )


def update_or_insert_requests(
    group: dict[date, list[SolarDayRequest]], existing_lookup: dict[datetime, SolarDay]
):
    min_time = datetime.min.time()
    for d, reqs in group.items():
        dt = datetime.combine(d, min_time)
        sd = existing_lookup.get(dt, SolarDay(date=dt))
        sd.upsert_values(convert_requests_to_time_values(reqs))
        yield sd
