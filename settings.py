from pydantic import BaseSettings, NoneStr

from util import parse_csv


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    api_key: NoneStr
    root_path: NoneStr
    origin_str: str = "http://localhost:3000"

    @property
    def origins(self):
        return parse_csv(self.origin_str)


settings = Settings()
