from sqlmodel import Session

from app import crud
from app.models import (UserCreate)
import pytest

@pytest.fixture
def create_user(db: Session):
    email = "ffff@gmail.com"
    password = "Testing#"
    is_editorial = False
    user_in = UserCreate(email=email, password=password, is_editor=is_editorial)
    user = crud.user.create_user(session=db, user_create=user_in)

    return user

def test_authenticate(db:Session,create_user):
    email = "ffff@gmail.com"
    password = "Testing#"
    login = crud.user.authenticate(session=db,email=email,password=password)
    assert login.email == email
    assert hasattr(login, "hashed_password")


def test_authenticate_failed_wrong_email(db:Session):
    email = "a@gmail.com"
    password = "Testing#"
    login = crud.user.authenticate(session=db,email=email,password=password)
    assert login is None

def test_authenticate_wrong_password(db:Session):
    email = "ffff@gmail.com"
    password = "Testin#"
    login = crud.user.authenticate(session=db,email=email,password=password)
    assert login is None
