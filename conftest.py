import pytest
from fastapi.testclient import TestClient

from app import app
from database import get_database


@pytest.fixture(scope="session")
def _database():
    from database import client

    return client.get_database("test_solar")


@pytest.fixture(scope="session")
def client(_database):
    app.dependency_overrides[get_database] = lambda: _database
    with TestClient(app=app) as c:
        yield c
