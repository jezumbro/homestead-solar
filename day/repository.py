from database import BulkRepository
from pydantic_mongo import AbstractRepository

from day.model import SolarDay


class DayRepository(AbstractRepository[SolarDay], BulkRepository):
    collection = "day"
