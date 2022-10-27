from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from controller import schemas, crud, model
from controller.api import deps
from controller.core import security, settings

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login(
        db: Session = Depends(deps.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> schemas.Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password!")
    token = security.create_access_token(user.id)
    return schemas.Token(access_token=token, token_type="bearer")


@router.post("/register", response_model=schemas.User)
def register(
        request: schemas.UserCreate,
        db: Session = Depends(deps.get_db)
) -> schemas.User:
    """
    Create a new user
    """
    user = crud.user.get_by_username(db, username=request.username)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with that username already exists!")

    user = crud.user.create(db, user=request)

    return user


@router.post("/test-token", response_model=schemas.User)
def test_token(
        current_user: model.User = Depends(deps.get_current_user)
) -> schemas.User:
    """
    Test access token
    """
    return current_user
