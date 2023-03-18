from datetime import date, datetime
from typing import Iterable

from database import BulkRepository
from pydantic_mongo import AbstractRepository

from day.model import SolarDay


class SolarDayRepository(AbstractRepository[SolarDay], BulkRepository):
    class Meta:
        collection_name = "solar_day"

    def find_one_by_date(self, d: date):
        min_time = datetime.min.time()
        query = {"date": datetime.combine(d, min_time)}
        return self.find_one_by(query)

    def find_by_dates(self, dates: Iterable[date]):
        min_time = datetime.min.time()
        query = {"date": {"$in": [datetime.combine(x, min_time) for x in dates]}}
        return self.find_by(query)
