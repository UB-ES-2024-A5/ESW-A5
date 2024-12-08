from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app import crud
from app.models import (Account, AccountBase, User, UserCreate, AccountUpdate,)
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

# Variable para almacenar datos entre pruebas
created_account_data = {}

def test_create_account_correctly(db: Session, create_user):
    user = create_user

    account_in = Account(id=user.id, bio="initial bio")
    account = crud.account.create_account(session=db, account=account_in)

    assert account.id is not None
    assert account.id == user.id
    assert account.bio == "initial bio"
    created_account_data["id"] = account.id
    created_account_data["bio"] = account.bio


def test_get_account_by_id(db: Session):
    account = crud.account.get_account_by_id(session=db, id=created_account_data["id"])

    assert account.id is not None
    assert account.id == created_account_data["id"]
    assert account.bio == created_account_data["bio"]

    non_existing_id = uuid4()
    account = crud.account.get_account_by_id(session=db, id=non_existing_id)
    assert account is None

def test_update_account(db: Session):
    # Caso 1: Actualizar una cuenta existente
    update_data = AccountUpdate(bio="Updated bio")
    account = crud.account.get_account_by_id(session=db, id=created_account_data["id"])
    updated_account = crud.account.update_account(session=db, db_account=account, account_in=update_data)
    assert updated_account.bio == "Updated bio"

