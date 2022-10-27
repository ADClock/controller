import random
import string

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from controller import model, crud
from controller.schemas import UserCreate


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def get_or_create_user(db: Session, username: str = random_lower_string()) -> model.User:
    db_user = crud.user.get_by_username(db, username=username)
    if db_user:
        return db_user
    else:
        return crud.user.create(db, obj_in=UserCreate(username=username, password=random_lower_string()))


def get_authentication_headers(client: TestClient,
                               username: str = "test",
                               password: str = "test") -> dict:
    r = client.post("/auth/register", json={"username": username, "password": password})
    r2 = client.post("/auth/login", data={"username": username, "password": password})
    return {"Authorization": "Bearer " + r2.json()['access_token']}
