""" Review related CRUD methods """

from typing import Any, List

from sqlmodel import Session, select
from fastapi import HTTPException

from app.api.deps import CurrentUser
from app.core.security import get_password_hash, verify_password
from app.models import (
    User, UserCreate, UserUpdate, Review, ReviewCreatePointBook, ReviewCreateComment,
    ReviewUpdatePointBook, ReviewUpdateComment, ReviewOut, Comment, CommentOut, CommentsOut, CommentUpdate, Book
)
import uuid


def convert_review_reviewOut(review: Review):
    reviewOut = ReviewOut(
        id=review.id,
        account_id=review.account_id,
        book_id=review.book_id,
        point_book=review.point_book,
        list_comments=[comment.text for comment in review.comments]  # Mapear los comments como strings
    )
    return reviewOut


def create_review_pb(session: Session, review: ReviewCreatePointBook, book: Book, current_user: User) -> Review:
    db_obj = Review(
        account_id=current_user.account.id,
        book_id=book.id,
        point_book=review.point_book,
    )
    # Afegim tant al account com en el book
    current_user.account.reviews.append(db_obj)
    book.reviews.append(db_obj)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_point_book(session: Session, review_in: ReviewUpdatePointBook, db_review: Review):
    db_review.point_book = review_in.point_book  # Actualizem la URL
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

def delete_point_book(session: Session, db_review: Review):
    db_review.point_book = None  # Actualizem la URL
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review


def is_delete_point_book(session: Session, db_review: Review):
    if db_review.point_book is None:
        return True
    return False


def create_review_empty(session: Session, book: Book, current_user: User):
    db_obj = Review(
        account_id=current_user.account.id,
        book_id=book.id,
        point_book=None,
    )
    # Afegim tant al account com en el book
    current_user.account.reviews.append(db_obj)
    book.reviews.append(db_obj)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_comment(session: Session, comment: ReviewUpdateComment, db_comment: Comment):
    db_comment.text = comment.text  # Actualizem la URL
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment


def add_comment(session: Session, review_in: ReviewCreateComment, db_review: Review) -> Book:
    comment = Comment(text=review_in.text)
    db_review.comments.append(comment)
    session.add(comment)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review


def delete_comment(session: Session, db_review: Review, comment_id: uuid.UUID):
    comment = get_comment_by_id(session=session, comment_id=comment_id)
    session.delete(comment)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

def get_comment_by_id(session: Session, comment_id: uuid.UUID) -> Comment:
    statement = select(Comment).where(Comment.id == comment_id)
    return session.exec(statement).first()


def get_review_by_id(session: Session, review_id: uuid.UUID) -> Review:
    statement = select(Review).where(Review.id == review_id)
    return session.exec(statement).first()


def get_review_by_comment_id(session: Session, comment_id: uuid.UUID) -> Review:
    comment = get_comment_by_id(session, comment_id)
    return get_review_by_id(session, comment.review_id)


def get_comments_by_review_id(session: Session, review_id: uuid.UUID) -> CommentsOut:
    review = get_review_by_id(session, review_id)
    comments = []
    cont = 0
    for comment in review.comments:
        comments.append(comment)
        cont += 1

    return CommentOut(comments=comments, cont=cont)


# Eliminar la review entera
def delete_review(session: Session, db_review: Review):
    for comment in db_review.comments:
        session.delete(comment)
    session.delete(db_review)
    session.commit()


# Actualizar el ranking del libro con la nueva review de point book
def update_rating(session: Session, book: Book, new_num_review: int):
    book.num_reviews += new_num_review
    if book.num_reviews < 0:
        book.num_reviews = 0

    total_points = sum(review.point_book for review in book.reviews if review.point_book is not None)

    if book.num_reviews > 0:
        book.rating = round(total_points / book.num_reviews, 1)
    else:
        book.rating = 0

    session.add(book)
    session.commit()
    session.refresh(book)


# Hay comments en una review
def there_are_comments(review: Review):
    cont = 0
    for comment in review.comments:
        cont += 1

    if cont > 0:
        return True
    return False


# Ha sido puntuado por el pointBook
def is_point_book(review: Review):
    if review.point_book is not None:
        return True
    return False


# Aquesta part de codi surt 9 vegades, per reduir linies de codi
def is_editor_and_review(session: Session, current_user: CurrentUser, book_id: uuid.UUID):
    if current_user.is_editor:
        raise HTTPException(
            status_code=400, detail="The user cannot be an editorial user."
        )
    statement = select(Review).where((Review.book_id == book_id) & (Review.account_id == current_user.account.id))
    db_review = session.exec(statement).first()

    return db_review

