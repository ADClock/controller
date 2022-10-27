from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from controller import crud
from controller.schemas import UserCreate, UserUpdate
from tests.utils.utils import random_lower_string


def test_create_user(db: Session) -> None:
    username = random_lower_string()
    user_in = UserCreate(username=username, password=random_lower_string())
    user = crud.user.create(db, user=user_in)
    assert user.username == username
    assert hasattr(user, "hashed_password")


def test_create_user_twice(db: Session) -> None:
    username = random_lower_string()
    user_in = UserCreate(username=username, password=random_lower_string())
    user_one = crud.user.create(db, user=user_in)
    assert user_one.username == username
    assert hasattr(user_one, "hashed_password")

    try:
        crud.user.create(db, user=user_in)
    except IntegrityError as err:
        assert "username" in err.args[0]
        return

    raise Exception("User two should fail with IntegrityError")


def test_update_user(db: Session) -> None:
    username = random_lower_string()
    user_in = UserCreate(username=username, password=random_lower_string())
    user = crud.user.create(db, user=user_in)
    assert user.username == username
    assert hasattr(user, "hashed_password")
    db.close()
    old_hash = user.hashed_password

    user_update = UserUpdate(password=random_lower_string())
    user2 = crud.user.update(db, db_obj=user, obj_in=user_update)
    print(user2.hashed_password)
    assert hasattr(user2, "hashed_password")
    assert user.id == user2.id
    assert old_hash != user2.hashed_password


def test_remove_user(db: Session) -> None:
    username = random_lower_string()
    user_in = UserCreate(username=username, password=random_lower_string())
    user = crud.user.create(db, user=user_in)
    assert user.username == username
    assert hasattr(user, "hashed_password")

    crud.user.remove(db, id=user.id)
    user2 = crud.user.get(db, id=user.id)
    assert user2 is None
