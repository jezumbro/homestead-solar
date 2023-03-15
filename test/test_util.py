from datetime import datetime

import pytest
from util import validate_has_timezone


@pytest.mark.parametrize(
    "dt,expected",
    [
        ("2023-03-01T06:00+00:00", "2023-03-01T06:00:00+00:00"),
        ("2023-03-01T12:00+06:00", "2023-03-01T06:00:00+00:00"),
        ("2023-03-01T00:00-06:00", "2023-03-01T06:00:00+00:00"),
    ],
)
def test_validate_has_timezone(dt, expected):
    output = validate_has_timezone(datetime.fromisoformat(dt))
    assert output.isoformat() == expected
