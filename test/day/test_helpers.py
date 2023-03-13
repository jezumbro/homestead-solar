import pytest
from more_itertools import first

from day.helpers import group_by_localized_date, update_or_insert_requests


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
    assert len(day.values) == 2
    assert day.id is None
