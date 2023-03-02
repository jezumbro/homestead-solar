from json import dumps, loads
from typing import Optional

from database import MongoModel
from pydantic import NoneStr
from rsa_helper import decrypt, encrypt


class Engine(MongoModel):
    user_id: str
    encrypted: NoneStr = None

    @property
    def tokens(self):
        return loads(decrypt(self.encrypted))

    def set_tokens(self, value: Optional[dict]):
        if value is None:
            self.encrypted = None
            return
        self.encrypted = encrypt(dumps(value))
