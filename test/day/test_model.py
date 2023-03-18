import pytest

from day.model import Temperature, Weather


@pytest.mark.parametrize(
    "weather,expected",
    (
        (None, None),
        (
            Weather(code="1", display="foo", temperature=Temperature(min=32, max=90)),
            Weather(code="1", display="foo", temperature=Temperature(min=32, max=90)),
        ),
    ),
)
def test_upsert_weather(solar_day_3_10, weather, expected):
    sd = solar_day_3_10
    assert sd.weather is None
    sd.upsert_weather(weather)
    assert sd.weather == expected


def test_upsert_none_doesnt_change_weather(solar_day_3_10):
    sd = solar_day_3_10
    sd.weather = Weather(
        code="1", display="foo", temperature=Temperature(min=32, max=90)
    )
    assert sd.weather is not None
    sd.upsert_weather(None)
    assert sd.weather is not None
