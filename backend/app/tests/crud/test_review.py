import pytest
from uuid import uuid4
from sqlmodel import Session
from app import crud
from app.models import (
    Review, ReviewCreatePointBook, ReviewUpdatePointBook, ReviewCreateComment,
    ReviewUpdateComment, User, UserCreate, Book, Comment, Account, BookCreate
)

review_data_fixtures = {}
# Fixtures
@pytest.fixture
def create_user(db: Session):
    email ="john.doe4@example.com"
    password = "asdfasdf"
    name = "John"
    surname = "Doe"
    is_editor = True

    user_in = UserCreate(email=email, password=password,is_editor=is_editor, name=name,surname=surname)
    user = crud.user.create_user(session=db, user_create=user_in)

    review_data_fixtures["user"] = user

    return user

@pytest.fixture
def create_account(db: Session, create_user):
    user_in = create_user

    account_in = Account(id=user_in.id)
    account = crud.account.create_account(session=db, account=account_in)

    review_data_fixtures["account"] = account

    return account,user_in

@pytest.fixture
def create_book(db: Session):

    existing_user = crud.user.get_user_by_email(session=db,email="john.doe4@example.com")
    existing_account = crud.account.get_account_by_id(session=db,id=existing_user.id)

    title = "BookN"
    author = "Damian"
    genre1 = "Fantasía"
    synopsis = "lorem ipsum"
    isbn = "7675453124320"
    account_id = existing_account.id
    price = 56.3
    publication_year = 2023
    links = []

    book_in = BookCreate(title=title,author=author,gender_main=genre1,synopsis=synopsis,isbn=isbn,account_id=account_id,price=price,publication_year=publication_year,links=links)
    book = crud.book.create_book(session=db,book=book_in, current_user=existing_user)

    review_data_fixtures["book"] = book

    return book

# Tests for create_review_pb

def test_create_review_point_book(db: Session, create_account, create_book):
    user, _ = create_account
    book = create_book

    review_data = ReviewCreatePointBook(point_book=4)
    review = crud.review.create_review_pb(session=db, review=review_data, book=book, current_user=review_data_fixtures["user"])

    assert review.id is not None
    assert review.account_id == user.id
    assert review.book_id == book.id
    assert review.point_book == 4

# Tests for update_point_book
def test_update_point_book(db: Session):
    review_data = ReviewCreatePointBook(point_book=3)
    review = crud.review.create_review_pb(session=db, review=review_data, book=review_data_fixtures["book"], current_user=review_data_fixtures["user"])

    update_data = ReviewUpdatePointBook(point_book=5)
    updated_review = crud.review.update_point_book(session=db, review_in=update_data, db_review=review)

    assert updated_review.point_book == 5

# Tests for delete_point_book
def test_delete_point_book(db: Session):
    review_data = ReviewCreatePointBook(point_book=3)
    review = crud.review.create_review_pb(session=db, review=review_data, book=review_data_fixtures["book"], current_user=review_data_fixtures["user"])

    deleted_review = crud.review.delete_point_book(session=db, db_review=review)
    assert deleted_review.point_book is None
    assert crud.review.is_delete_point_book(session=db, db_review=deleted_review) is True

# Tests for add_comment
def test_add_comment_to_review(db: Session):
    review_data = ReviewCreatePointBook(point_book=4)
    review = crud.review.create_review_pb(session=db, review=review_data, book=review_data_fixtures["book"], current_user=review_data_fixtures["user"])

    comment_data = ReviewCreateComment(text="Great book!")
    updated_review = crud.review.add_comment(session=db, review_in=comment_data, db_review=review)

    assert len(updated_review.comments) == 1
    assert updated_review.comments[0].text == "Great book!"

# Tests for delete_comment
def test_delete_comment_from_review(db: Session):
    review_data = ReviewCreatePointBook(point_book=4)
    review = crud.review.create_review_pb(session=db, review=review_data, book=review_data_fixtures["book"], current_user=review_data_fixtures["user"])

    comment_data = ReviewCreateComment(text="Good book!")
    updated_review = crud.review.add_comment(session=db, review_in=comment_data, db_review=review)

    comment = updated_review.comments[0]
    updated_review_after_deletion = crud.review.delete_comment(session=db, db_review=review, comment_id=comment.id)

    assert len(updated_review_after_deletion.comments) == 0
