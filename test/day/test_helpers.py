from datetime import datetime

import pytest
from more_itertools import first

from day.helpers import (
    create_solar_day,
    group_by_localized_date,
    update_or_insert_requests,
)


@pytest.fixture
def single_day_group(single_day_request):
    return group_by_localized_date(single_day_request)


def test_unique_days_from_requests_single_day(single_day_group):
    assert sorted(x.isoformat() for x in single_day_group.keys()) == ["2023-03-10"]


def test_unique_days_from_requests_multiple_days(multi_day_request):
    days = group_by_localized_date(multi_day_request)
    assert sorted(x.isoformat() for x in days.keys()) == ["2023-03-09", "2023-03-10"]


def test_upsert_request(single_day_group):
    days = list(update_or_insert_requests(single_day_group, {}))
    assert len(days) == 1
    day = first(days)
    assert day.id is None
    assert len(day.values) == 4


def test_create_solar_day(solar_client):
    sd = create_solar_day(datetime(2023, 3, 18), solar_client)
    assert sd.date.date().isoformat() == "2023-03-18"
    assert sd.times
