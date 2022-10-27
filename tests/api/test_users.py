from fastapi import status
from fastapi.testclient import TestClient

from tests.utils.utils import get_authentication_headers


def test_users_get_all_without_authentication(client: TestClient):
    r = client.get("/users/")
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_users_get_all_with_authentication(client: TestClient):
    header = get_authentication_headers(client)
    r = client.get("/users/", headers=header)
    assert r.status_code == status.HTTP_200_OK
