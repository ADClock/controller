from datetime import timedelta

from controller.core import security


def test_password_hash_equal():
    password = "my-secure-password"
    hashed_password = security.get_password_hash(password)
    assert security.verify_password(password, hashed_password)


def test_password_hash_non_equal():
    password = "my-secure-password"
    hashed_password = security.get_password_hash(password)
    assert not security.verify_password(password + "1", hashed_password)


def test_create_access_token_no_expires():
    access_token = security.create_access_token(subject="tester")
    assert access_token


def test_create_access_token_expires():
    access_token = security.create_access_token(subject="tester", expires_delta=timedelta(seconds=1))
    assert access_token
