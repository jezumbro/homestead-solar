from datetime import datetime
from typing import Union

from dateutil.tz import tz


def parse_csv(string: Union[str, list[str]]) -> list[str]:
    if isinstance(string, list):
        return string
    return string.split(",")


def add_utc(dt: datetime) -> datetime:
    return dt.replace(tzinfo=tz.tzutc())


def has_timezone_information(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError("must provide timezone information")
    return dt.astimezone(tz.tzutc())


def no_timezone_information(dt):
    if dt.tzinfo is not None:
        raise ValueError("must provide utc timezone with no information")
    return dt


def remove_timezone(dt: datetime):
    return dt.replace(tzinfo=None)


def to_localized_date(dt):
    return dt.astimezone(tz.gettz("America/Chicago")).date()
