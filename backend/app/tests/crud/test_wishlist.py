from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app import crud
from app.core.security import verify_password
from app.models import (User, UserCreate, UserUpdate, Account, WishListCreate, WishListUpdate)
from app.tests.utils.utils import random_email, random_lower_string
import pytest

@pytest.fixture

def create_user(db: Session):
    email ="john.doe3@example.com"
    password = "asdfasdf"
    name = "John"
    surname = "Doe"
    is_editor = False

    user_in = UserCreate(email=email, password=password,is_editor=is_editor, name=name,surname=surname)
    user = crud.user.create_user(session=db, user_create=user_in)

    return user

@pytest.fixture
def create_account(db: Session, create_user):
    user_in = create_user

    account_in = Account(id=user_in.id)
    account = crud.account.create_account(session=db, account=account_in)

    return account,user_in

def test_create_wishlist(db:Session, create_account):
    account, user = create_account
    name = "Wishlist 1"
    description = "Wishlist de libros de fantasia"

    wishlist_in = WishListCreate(name=name, description=description)
    wishlist_out = crud.wishlist.create_wishlist(session=db, wishlist=wishlist_in,current_user=user)

    assert wishlist_out.name == name

def test_update_wishlist(db:Session):
    user = crud.user.get_user_by_email(session=db,email="john.doe3@example.com")

    name = "Wishlist 1"
    description = "Wishlist de libros de fantasia"

    wishlist_in = WishListCreate(name=name, description=description)
    wishlist_out = crud.wishlist.create_wishlist(session=db, wishlist=wishlist_in,current_user=user)

    assert wishlist_out.name == name
    assert wishlist_out.description == description

    
    description = "Regalos de navidad"
    wishlist_in = WishListUpdate(description=description)
    wishlist_out2 = crud.wishlist.update_wishlist(session=db, db_wishlist=wishlist_out,wishlist_in=wishlist_in)

    assert wishlist_out2.name == name
    assert wishlist_out2.description == description
    assert wishlist_out2.id == wishlist_out.id




