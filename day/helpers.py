from datetime import date, datetime
from typing import Iterable

from client.sunrise_sunset import SolarClient
from more_itertools import map_reduce
from settings import settings
from util import to_localized_date

from day.model import SolarDay, SolarTimes, SunriseSunset, TimeValue
from day.request_schema import SolarDayRequest


def create_solar_day(d: date, client: SolarClient) -> SolarDay:
    resp = client.get_times(d, settings.latitude, settings.longitude)
    return SolarDay(
        date=datetime.combine(d, datetime.min.time()),
        times=SolarTimes(
            solar_noon=resp.solar_noon,
            local=SunriseSunset(
                sunrise=resp.sunrise,
                sunset=resp.sunset,
            ),
            civil=SunriseSunset(
                sunrise=resp.civil_twilight_begin,
                sunset=resp.civil_twilight_end,
            ),
            nautical=SunriseSunset(
                sunrise=resp.nautical_twilight_begin,
                sunset=resp.nautical_twilight_end,
            ),
            astronomical=SunriseSunset(
                sunrise=resp.astronomical_twilight_begin,
                sunset=resp.astronomical_twilight_end,
            ),
        ),
    )


def by_localized_date(req: SolarDayRequest) -> date:
    return to_localized_date(req.start_date)


def filter_nones(reqs: list[SolarDayRequest]):
    return (x for x in reqs if x.value is not None)


def group_by_localized_date(
    reqs: list[SolarDayRequest],
) -> dict[date, Iterable[SolarDayRequest]]:
    return map_reduce(reqs, keyfunc=by_localized_date, reducefunc=filter_nones)


def convert_requests_to_time_values(
    reqs: Iterable[SolarDayRequest],
) -> Iterable[TimeValue]:
    for req in reqs:
        if req.value is None:
            continue
        yield TimeValue(
            start_date=req.start_date.replace(tzinfo=None),
            end_date=req.end_date.replace(tzinfo=None),
            value=req.value,
        )


def update_or_insert_requests(
    group: dict[date, Iterable[SolarDayRequest]],
    existing_lookup: dict[datetime, SolarDay],
):
    min_time = datetime.min.time()
    for d, reqs in group.items():
        dt = datetime.combine(d, min_time)
        sd = existing_lookup.get(dt, SolarDay(date=dt))
        sd.upsert_values(convert_requests_to_time_values(reqs))
        yield sd
