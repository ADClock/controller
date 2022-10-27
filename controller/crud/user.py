from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from controller.core import security
from controller.crud.base import CRUDBase
from controller.model import User
from controller.schemas import UserCreate, UserUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, user: UserCreate) -> User:
        db_obj = User(
            username=user.username,
            hashed_password=security.get_password_hash(user.password)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        obj_data = jsonable_encoder(obj_in)
        if obj_data['password']:
            obj_data['hashed_password'] = security.get_password_hash(obj_in.password)
        return super().update(db, db_obj=db_obj, obj_in=obj_data)

    def authenticate(self, db: Session, *, username: str, password: str):
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not security.verify_password(plain_password=password, hashed_password=user.hashed_password):
            return None
        return user


user = CRUDUser(User)
