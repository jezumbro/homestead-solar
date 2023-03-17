from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator
from util import has_timezone_information


class SolarDayRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    value: Optional[float] = None

    _validate_dt = validator("start_date", "end_date", allow_reuse=True)(
        has_timezone_information
    )
