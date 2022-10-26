from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from controller import crud
from tests.utils.utils import random_lower_string


def get_register_payload():
    return {"username": random_lower_string(), "password": random_lower_string()}


def test_register_endpoint(client: TestClient, db: Session):
    payload = get_register_payload()
    r = client.post("/auth/register", json=payload)
    new_user = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert new_user
    assert new_user['username'] == payload['username']
    db_user = crud.user.get_by_username(db=db, username=payload['username'])
    assert db_user


def test_register_endpoint_existing_user(client: TestClient):
    payload = get_register_payload()
    r = client.post("/auth/register", json=payload)
    new_user = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert new_user
    assert new_user['username'] == payload['username']

    r2 = client.post("/auth/register", json=payload)
    assert r2.status_code == status.HTTP_400_BAD_REQUEST


def test_login_endpoint(client: TestClient):
    payload = get_register_payload()
    r = client.post("/auth/register", json=payload)
    new_user = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert new_user
    assert new_user['username'] == payload['username']

    r2 = client.post("/auth/login", data=payload)
    assert r2.status_code == status.HTTP_200_OK
    assert r2.json()['access_token']


def test_login_endpoint_unknown_user(client: TestClient):
    payload = get_register_payload()
    r = client.post("/auth/login", data=payload)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_token_endpoint_without_token(client: TestClient):
    r = client.post("/auth/test-token")
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_token_endpoint(client: TestClient):
    payload = get_register_payload()
    r = client.post("/auth/register", json=payload)
    new_user = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert new_user
    assert new_user['username'] == payload['username']

    r2 = client.post("/auth/login", data=payload)
    assert r2.status_code == status.HTTP_200_OK
    assert r2.json()['access_token']

    r3 = client.post("/auth/test-token", headers={"Authorization": f"Bearer {r2.json()['access_token']}"})
    assert r3.status_code == status.HTTP_200_OK
    assert r3.json()['username'] == payload['username']


def test_test_token_endpoint_with_invalid_token(client: TestClient):
    r = client.post("/auth/test-token", headers={"Authorization": "Bearer invalid"})
    assert r.status_code == status.HTTP_403_FORBIDDEN
