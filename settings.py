from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, HttpUrl, MongoDsn, NoneStr

from util import parse_csv

load_dotenv()


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    root_path: NoneStr = None

    origin_str: str = "http://localhost:3000"

    client_id: NoneStr = None

    mongo_dsn: MongoDsn = "mongodb://localhost:27017"
    db_name: str = "solar"

    sentry_dsn: Optional[HttpUrl] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @property
    def origins(self):
        return parse_csv(self.origin_str)


settings = Settings()
