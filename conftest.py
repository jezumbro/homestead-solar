from datetime import date

import pytest
from fastapi.testclient import TestClient

from app import app
from client.sunrise_sunset import AbstractSolarClient, SolarResponse, get_solar_client
from database import get_database


@pytest.fixture(scope="session")
def _database():
    from database import client

    return client.get_database("test_solar")


class FakeSolarClient(AbstractSolarClient):
    def __init__(self):
        super().__init__("http://test.com")

    def get_times(self, d: date, latitude: float, longitude: float):
        return SolarResponse.parse_obj(
            {
                "astronomical_twilight_begin": "2023-03-18T10:56:15+00:00",
                "astronomical_twilight_end": "2023-03-19T01:50:59+00:00",
                "civil_twilight_begin": "2023-03-18T11:56:20+00:00",
                "civil_twilight_end": "2023-03-19T00:50:54+00:00",
                "day_length": 43561,
                "nautical_twilight_begin": "2023-03-18T11:26:28+00:00",
                "nautical_twilight_end": "2023-03-19T01:20:46+00:00",
                "solar_noon": "2023-03-18T18:23:37+00:00",
                "sunrise": "2023-03-18T12:20:37+00:00",
                "sunset": "2023-03-19T00:26:38+00:00",
            }
        )


@pytest.fixture(scope="session")
def solar_client():
    return FakeSolarClient()


@pytest.fixture(scope="session")
def client(_database, solar_client):
    app.dependency_overrides[get_solar_client] = lambda: solar_client
    app.dependency_overrides[get_database] = lambda: _database
    with TestClient(app=app) as c:
        yield c
