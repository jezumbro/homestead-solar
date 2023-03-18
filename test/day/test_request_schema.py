from datetime import date

import pytest
from pydantic import ValidationError

from day.request_schema import CreateSolarDayRequest


def test_does_not_raise_value_error(
    single_day_request,
):
    d = date.fromisoformat("2023-03-10")
    _ = CreateSolarDayRequest(date=d, values=single_day_request)


def test_raise_value_error_if_date_and_values_are_not_on_the_same_day(
    multi_day_request,
):
    d = date.fromisoformat("2023-03-10")
    with pytest.raises(ValidationError):
        _ = CreateSolarDayRequest(date=d, values=multi_day_request)
