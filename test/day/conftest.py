import pytest

from day.request_schema import SolarDayRequest


@pytest.fixture
def multi_day_request():
    return [
        SolarDayRequest(
            start_date="2023-03-09T00:00-06:00",
            end_date="2023-03-09T00:15-06:00",
            value=3,
        ),
        SolarDayRequest(
            start_date="2023-03-10T06:15-00:00",
            end_date="2023-03-10T06:30-00:00",
            value=1,
        ),
    ]


@pytest.fixture
def single_day_request():
    return [
        SolarDayRequest(
            start_date="2023-03-10T00:00-06:00",
            end_date="2023-03-10T00:15-06:00",
            value=0,
        ),
        SolarDayRequest(
            start_date="2023-03-10T06:15-00:00",
            end_date="2023-03-10T06:30-00:00",
            value=1,
        ),
    ]
