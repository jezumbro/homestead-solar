from database import BulkRepository
from pydantic_mongo import AbstractRepository

from day.model import SolarDay


class SolarDayRepository(AbstractRepository[SolarDay], BulkRepository):
    class Meta:
        collection_name = "solar_day"
