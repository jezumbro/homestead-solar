from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, HttpUrl, MongoDsn, NoneStr

load_dotenv()


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    root_path: NoneStr = None

    origin_str: str = "http://localhost:3000"

    client_id: NoneStr = None

    mongo_dsn: str = "mongodb://localhost:27017"
    db_name: str = "solar"

    sentry_dsn: Optional[HttpUrl] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @property
    def origins(self):
        return self.origin_str.split(",")


settings = Settings()
