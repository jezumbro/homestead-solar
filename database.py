from typing import Iterable

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseConfig, BaseModel
from pymongo import InsertOne, MongoClient, UpdateOne
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import BulkWriteResult

from settings import settings

client = MongoClient(host=settings.db_host, port=settings.db_port)


def get_database() -> Database:
    return client[settings.db_name]


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoModel(BaseModel):
    id: OID = None

    class Config(BaseConfig):
        orm_mode = True
        json_encoders = {ObjectId: lambda oid: str(oid)}


class BulkRepository:
    def get_collection(self) -> Collection:
        ...

    def count(self, query=None):
        return self.get_collection().count_documents(query or {})

    @staticmethod
    def to_update(model: MongoModel):
        if model.id:
            return UpdateOne(
                {"_id": model.id},
                {"$set": model.dict(exclude={"id"})},
            )
        return InsertOne(model.dict())

    def bulk_upsert(self, documents: Iterable):
        if updates := [self.to_update(x) for x in documents if x]:
            return self.get_collection().bulk_write(updates)
        return BulkWriteResult(bulk_api_result={}, acknowledged=True)

    def delete_many(self, query=None):
        return self.get_collection().delete_many(query or {})
