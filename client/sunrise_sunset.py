from abc import ABC
from datetime import date, datetime
from pprint import pprint
from typing import Optional

import requests
from pydantic import BaseModel


class SolarResponse(BaseModel):
    sunrise: datetime
    sunset: datetime
    solar_noon: datetime
    nautical_twilight_begin: datetime
    nautical_twilight_end: datetime
    civil_twilight_begin: datetime
    civil_twilight_end: datetime
    astronomical_twilight_begin: datetime
    astronomical_twilight_end: datetime


class AbstractSolarClient(ABC):
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or "https://api.sunrise-sunset.org"

    def url(self, endpoint: str):
        if not endpoint.startswith("/"):
            raise ValueError("Endpoint must start with '/'")
        return self.base_url + endpoint

    def get_times(self, d: date, latitude: float, longitude: float) -> SolarResponse:
        raise NotImplementedError


class SolarClient(AbstractSolarClient):
    def __init__(self, base_url: Optional[str] = None):
        super().__init__(base_url)

    def url(self, endpoint: str):
        if not endpoint.startswith("/"):
            raise ValueError("Endpoint must start with '/'")
        return self.base_url + endpoint

    def get_times(self, d: date, latitude: float, longitude: float) -> SolarResponse:
        resp = requests.get(
            self.url("/json"),
            params={
                "lat": latitude,
                "lng": longitude,
                "date": d.isoformat(),
                "formatted": 0,
            },
        )
        return SolarResponse.parse_obj(resp.json()["results"])


def get_solar_client():
    return SolarClient()
