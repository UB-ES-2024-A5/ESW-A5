from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app import crud
from app.core.security import verify_password
from app.models import (User, UserCreate, UserUpdate)
from app.tests.utils.utils import random_email, random_lower_string


def test_create_editorial(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    is_editorial = True
    user_in = UserCreate(email=email, password=password, is_editor=is_editorial)
    user = crud.user.create_user(session=db, user_create=user_in)
    assert user.email == email
    assert user.is_editor == True
    assert hasattr(user, "hashed_password")


def test_get_editorial(db: Session) -> None:
    password = random_lower_string()
    username = random_email()
    is_editorial = True
    user_in = UserCreate(email=username, password=password, is_superuser=True, is_editor=is_editorial)
    user = crud.user.create_user(session=db, user_create=user_in)
    user_2 = db.get(User, user.id)
    assert user_2
    assert user.email == user_2.email
    assert user.is_editor == True
    assert jsonable_encoder(user) == jsonable_encoder(user_2)