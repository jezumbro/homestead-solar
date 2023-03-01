import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app=app) as c:
        yield c
