from datetime import datetime

import pytest

from day.model import SolarDay, TimeValue
from day.repository import SolarDayRepository
from day.request_schema import SolarDayRequest


@pytest.fixture
def solar_repo(_database):
    repo = SolarDayRepository(_database)
    repo.delete_many()
    return repo


@pytest.fixture()
def solar_day_3_10(solar_repo):
    sd = SolarDay(
        date=datetime(2023, 3, 10),
        values=[
            TimeValue(
                end_date=datetime(2023, 3, 10, 12),
                start_date=datetime(2023, 3, 10, 12, 15),
                value=100,
            )
        ],
    )
    solar_repo.save(sd)
    return sd


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
        SolarDayRequest(
            start_date="2023-03-11T05:15-00:00",
            end_date="2023-03-11T05:30-00:00",
            value=1,
        ),
        SolarDayRequest(
            start_date="2023-03-11T05:45-00:00",
            end_date="2023-03-11T06:00-00:00",
            value=3,
        ),
    ]
