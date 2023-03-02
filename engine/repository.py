from database import BulkRepository
from pydantic_mongo import AbstractRepository

from engine.model import Engine


class EngineRepo(AbstractRepository[Engine], BulkRepository):
    class Meta:
        collection_name = "engine"
