from typing import Generator

import pytest
from fastapi.testclient import TestClient

from controller.app import app
from controller.database.session import SessionLocal


@pytest.fixture(scope="function")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
