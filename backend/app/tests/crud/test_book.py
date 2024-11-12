from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app import crud
from app.models import (Book, BookBase, BookCreate, UserCreate, Account, LinkBase)
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

@pytest.fixture
def create_account(db: Session, create_user):
    user_in = create_user

    account_in = Account(id=user_in.id)
    account = crud.account.create_account(session=db, account=account_in)

    return account


def test_create_book_all_mandatory_fields(db:Session,):
    existing_account = db.exec(Account).first()

    title = "Book1"
    author = "Pau"
    gender_main = "Fantasía"
    synopsis = "lorem ipsum"
    isbn = "7675453127980"
    account_id_in = existing_account.id

    link1 = LinkBase(url="http://example.com/link1")
    link2 = LinkBase(url="http://example.com/link2")
    links = [link1, link2]

    book_in = BookCreate(title=title,author=author,gender_main=gender_main,synopsis=synopsis,isbn=isbn,account_id=account_id_in,links=links)
    book = crud.book.create_book(session=db,book_create=book_in)

    assert book.title == title
    assert book.isbn == isbn
    assert len(book.links) == 2

def test_create_book(db:Session,create_account):

    existing_account = db.exec(Account).first()

    title = "Book2"
    author = "Pau"
    genre1 = "Fantasía"
    synopsis = "lorem ipsum"
    isbn = "7675453127981"
    account_id_in = existing_account.id
    price = 56.3
    publication_year = 2023

    book_in = BookCreate(title=title,author=author,genre1=genre1,synopsis=synopsis,isbn=isbn,account_id=account_id_in,price=price,publication_year=publication_year)
    book = crud.book.create_book(session=db,book_create=book_in)

    assert book.title == title
    assert book.isbn == isbn


def test_create_book_isbn_already_in_db(db:Session,create_account):

    existing_account = db.exec(Account).first()

    title = "Book6"
    author = "Dani"
    genre1 = "Amor"
    synopsis = "lorem ipsum"
    isbn = "7675453127980"
    account_id_in = existing_account.id
    price = 30
    publication_year = 1990

    book_in = BookCreate(title=title,author=author,genre1=genre1,synopsis=synopsis,isbn=isbn,account_id=account_id_in,price=price,publication_year=publication_year)
    
    with pytest.raises(IntegrityError):
        book = crud.book.create_book(session=db,book_create=book_in)

def test_get_book_by_id(db:Session, create_account):
    existing_account = db.exec(Account).first()

    title = "Book5"
    author = "Pau"
    genre1 = "Fantasía"
    synopsis = "lorem ipsum"
    isbn = "7675453127941"
    account_id_in = existing_account.id
    price = 56.3
    publication_year = 2023

    book_in = BookCreate(title=title,author=author,genre1=genre1,synopsis=synopsis,isbn=isbn,account_id=account_id_in,price=price,publication_year=publication_year)
    book = crud.book.create_book(session=db,book_create=book_in)

    book_out = crud.book.get_book_by_id(session=db, id=book.id)
    assert book_out.title == book.title
    assert book_out.isbn == book.isbn



    






    


