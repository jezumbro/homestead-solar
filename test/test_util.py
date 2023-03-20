from datetime import datetime

import pytest
from util import (
    has_timezone_information,
    no_timezone_information,
    remove_timezone,
    to_localized_date,
)


def test_validate_has_timezone_raises():
    with pytest.raises(ValueError):
        _ = has_timezone_information(datetime.fromisoformat("2023-03-20T00:00"))


@pytest.mark.parametrize(
    "dt,expected",
    [
        ("2023-03-01T06:00+00:00", "2023-03-01T06:00:00+00:00"),
        ("2023-03-01T12:00+06:00", "2023-03-01T06:00:00+00:00"),
        ("2023-03-01T00:00-06:00", "2023-03-01T06:00:00+00:00"),
        ("2023-03-14T23:45-05:00", "2023-03-15T04:45:00+00:00"),
        ("2023-03-13T19:00-05:00", "2023-03-14T00:00:00+00:00"),
    ],
)
def test_validate_has_timezone(dt, expected):
    output = has_timezone_information(datetime.fromisoformat(dt))
    assert output.isoformat() == expected


@pytest.mark.parametrize(
    "dt,expected",
    [
        ("2023-03-14T00:00:00+00:00", "2023-03-13"),
        ("2023-03-15T04:45:00+00:00", "2023-03-14"),
        ("2023-03-15T05:00:00+00:00", "2023-03-15"),
    ],
)
def test_by_localized_date(dt, expected):
    assert to_localized_date(datetime.fromisoformat(dt)).isoformat() == expected


def test_no_timezone_raises():
    with pytest.raises(ValueError):
        _ = no_timezone_information(datetime.fromisoformat("2023-03-14T00:00:00+00:00"))


@pytest.mark.parametrize(
    "dt",
    [
        "2023-03-14T00:00:00+00:00",
        "2023-03-15T04:45:00+00:00",
        "2023-03-15T05:00:00+00:00",
    ],
)
def test_remove_timezone(dt):
    expected = datetime.fromisoformat(dt).replace(tzinfo=None)
    assert remove_timezone(datetime.fromisoformat(dt)) == expected
