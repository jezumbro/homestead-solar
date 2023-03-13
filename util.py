from datetime import datetime
from typing import Union

from dateutil import tz


def parse_csv(string: Union[str, list[str]]) -> list[str]:
    if isinstance(string, list):
        return string
    return string.split(",")


def add_utc(dt: datetime) -> datetime:
    return dt.replace(tzinfo=tz.tzutc())


def validate_has_timezone(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError("must provide timezone information")
    return dt.astimezone(tz.tzutc())


def no_tz_info(dt):
    if dt.tzinfo is not None:
        raise ValueError("must provide utc timezone with no information")
    return dt
