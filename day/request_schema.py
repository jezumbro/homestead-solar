from datetime import datetime

from pydantic import BaseModel, validator
from util import validate_has_timezone


class SolarDayRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    value: float

    _validate_dt = validator("start_date", "end_date", allow_reuse=True)(
        validate_has_timezone
    )
