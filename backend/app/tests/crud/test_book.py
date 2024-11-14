from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app import crud
from app.models import (Book, BookBase, BookCreate, UserCreate, Account, LinkBase)
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from uuid import uuid4
import pytest

@pytest.fixture
def create_user(db: Session):
    email ="john.doe2@example.com"
    password = "asdfasdf"
    name = "John"
    surname = "Doe"
    is_editor = True

    user_in = UserCreate(email=email, password=password,is_editor=is_editor, name=name,surname=surname)
    user = crud.user.create_user(session=db, user_create=user_in)

    return user

@pytest.fixture
def create_account(db: Session, create_user):
    user_in = create_user

    account_in = Account(id=user_in.id)
    account = crud.account.create_account(session=db, account=account_in)

    return account,user_in


def test_create_book_all_mandatory_fields(db:Session,create_account):
    db.rollback()
    existing_account,current_user = create_account
    assert existing_account.id != None
    title = "Book1"
    author = "Pau"
    gender_main = "Fantasía"
    synopsis = "lorem ipsum"
    isbn = "7675453127980"
    account_id_in = existing_account.id
    links = ["https://bookimg.com"]

    book_in = BookCreate(title=title,author=author,gender_main=gender_main,synopsis=synopsis,isbn=isbn,account_id=account_id_in,links=links)
    book = crud.book.create_book(session=db,book=book_in,current_user=current_user)
    book_final = crud.book.add_links(session=db,book=book_in,db_obj=book)

    assert book_final.title == title
    assert str(book_final.isbn) == isbn
    assert len(book_final.links) == 1

def test_create_book(db:Session):

    existing_user = crud.user.get_user_by_email(session=db,email="john.doe2@example.com")
    existing_account = crud.account.get_account_by_id(session=db,id=existing_user.id)

    title = "Book2"
    author = "Pau"
    genre1 = "Fantasía"
    synopsis = "lorem ipsum"
    isbn = "7675453127981"
    account_id = existing_account.id
    price = 56.3
    publication_year = 2023
    links = []

    book_in = BookCreate(title=title,author=author,gender_main=genre1,synopsis=synopsis,isbn=isbn,account_id=account_id,price=price,publication_year=publication_year,links=links)
    book = crud.book.create_book(session=db,book=book_in, current_user=existing_user)

    assert book.title == title
    assert str(book.isbn) == isbn


def test_create_book_isbn_already_in_db(db:Session):

    existing_user = crud.user.get_user_by_email(session=db,email="john.doe2@example.com")
    existing_account = crud.account.get_account_by_id(session=db,id=existing_user.id)

    title = "Book2"
    author = "Pau"
    genre1 = "Fantasía"
    synopsis = "lorem ipsum"
    isbn = "7675453127981"
    account_id = existing_account.id
    price = 56.3
    publication_year = 2023
    links = []

    book_in = BookCreate(title=title,author=author,gender_main=genre1,synopsis=synopsis,isbn=isbn,account_id=account_id,price=price,publication_year=publication_year,links=links)
    
    with pytest.raises(IntegrityError):
        try:
            book = crud.book.create_book(session=db, book=book_in, current_user=existing_user)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

def test_get_book_by_id(db:Session):
    existing_user = crud.user.get_user_by_email(session=db,email="john.doe2@example.com")
    existing_account = crud.account.get_account_by_id(session=db,id=existing_user.id)

    title = "Book5"
    author = "Pau"
    genre1 = "Fantasía"
    synopsis = "lorem ipsum"
    isbn = "733353127941"
    account_id_in = existing_account.id
    price = 56.3
    publication_year = 2023
    links = []

    book_in = BookCreate(title=title,author=author,gender_main=genre1,synopsis=synopsis,isbn=isbn,account_id=account_id_in,price=price,publication_year=publication_year,links=links)
    book = crud.book.create_book(session=db,book=book_in,current_user=existing_user)

    book_out = crud.book.read_book_by_id(session=db, id=book.id)
    assert book_out.title == book.title
    assert book_out.isbn == book.isbn


def test_create_book_with_isbn_with_less_than_10_digits(db:Session):

    existing_user = crud.user.get_user_by_email(session=db,email="john.doe2@example.com")
    existing_account = crud.account.get_account_by_id(session=db,id=existing_user.id)

    title = "Book2"
    author = "Pau"
    genre1 = "Fantasía"
    synopsis = "lorem ipsum"
    isbn = "81"
    account_id = existing_account.id
    price = 56.3
    publication_year = 2023
    links = []

    
    with pytest.raises(ValidationError):
        book_in = BookCreate(title=title,author=author,gender_main=genre1,synopsis=synopsis,isbn=isbn,account_id=account_id,price=price,publication_year=publication_year,links=links)

        
def test_create_book_with_isbn_with_more_than_13_digits(db:Session):

    existing_user = crud.user.get_user_by_email(session=db,email="john.doe2@example.com")
    existing_account = crud.account.get_account_by_id(session=db,id=existing_user.id)

    title = "Book2"
    author = "Pau"
    genre1 = "Fantasía"
    synopsis = "lorem ipsum"
    isbn = "81191919191919"
    account_id = existing_account.id
    price = 56.3
    publication_year = 2023
    links = []

    
    with pytest.raises(ValidationError):
        book_in = BookCreate(title=title,author=author,gender_main=genre1,synopsis=synopsis,isbn=isbn,account_id=account_id,price=price,publication_year=publication_year,links=links)



    






    


