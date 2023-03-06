from datetime import datetime
from typing import Iterable

from database import MongoModel
from pydantic import BaseModel, Field


class DatetimeValue(BaseModel):
    datetime: datetime
    value: float


class SolarDay(MongoModel):
    date: datetime
    values: list[DatetimeValue] = Field(default_factory=list)

    def existing_lookup(self):
        return {x.datetime: x for x in self.values}

    def upsert_values(self, new_values: Iterable[DatetimeValue]):
        existing_lkp = self.existing_lookup()
        seen = set()
        for row in new_values:
            if row.datetime in seen:
                continue
            seen.add(row.datetime)
            if existing := existing_lkp.get(row.datetime):
                existing.value = row.value
                continue
            self.values.append(row)
        self.values.sort(key=lambda x: x.datetime)
