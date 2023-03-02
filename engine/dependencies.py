from database import get_database
from fastapi import Depends

from engine.repository import EngineRepo


def get_engine_repo(database=Depends(get_database)):
    return EngineRepo(database)
