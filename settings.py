from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, FilePath, NoneStr

from util import parse_csv

load_dotenv()


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    api_key: NoneStr = None
    root_path: NoneStr = None

    origin_str: str = "http://localhost:3000"

    client_id: NoneStr = None
    client_secret: NoneStr = None
    user_id: NoneStr = None

    db_host: str = "localhost"
    db_port: int = 27017
    db_name: str = "solar"

    rsa_file: Optional[FilePath] = None

    @property
    def origins(self):
        return parse_csv(self.origin_str)


settings = Settings()
