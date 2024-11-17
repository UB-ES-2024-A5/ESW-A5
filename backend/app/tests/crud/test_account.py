from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app import crud
from app.models import (Account, AccountBase, User, UserCreate)
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
import pytest


@pytest.fixture
def create_user(db: Session):
    email ="john.doe@example.com"
    password = "asdfasdf"
    name = "John"
    surname = "Doe"
    is_editor = False

    user_in = UserCreate(email=email, password=password,is_editor=is_editor, name=name,surname=surname)
    user = crud.user.create_user(session=db, user_create=user_in)

    return user

def test_create_account_correctly(db: Session,create_user):
    user = create_user

    account_in = Account(id=user.id)
    account = crud.account.create_account(session=db, account=account_in)

    assert account.id is not None
    assert account.id == user.id



