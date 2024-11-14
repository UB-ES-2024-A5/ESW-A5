""" Reviews management routes """

import uuid

from typing import Any

from sqlmodel import col, delete, func, select
from fastapi import APIRouter, Depends, HTTPException

from app import crud
from app.api.deps import (
    CurrentUser, SessionDep, get_current_active_superuser,
)

from app.models import (
    Review, ReviewCreatePointBook, ReviewCreateComment, ReviewUpdatePointBook, ReviewUpdateComment,
    ReviewOut, ReviewsOut, User, Message, Account, Comment, CommentOut, CommentsOut, CommentUpdate
)

router = APIRouter()

# Tindra dependecia de super user
@router.get("/", response_model=ReviewsOut)
def read_all_reviews(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all reviews.
    """
    count_statement = select(func.count()).select_from(Review)
    count = session.exec(count_statement).one()

    statement = select(Review).offset(skip).limit(limit)
    reviews = session.exec(statement).all()

    # Esto es necessario para cnvertir los Book, en BookOut donde contiene una lista de strings con url de los links
    reviews_out = [crud.review.convert_review_reviewOut(review=review) for review in reviews]

    return ReviewsOut(data=reviews_out, count=count)

@router.get("/my_books", response_model=ReviewsOut)
def read_all_my_reviews(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all reviews for the current user, lector user only.
    """
    if current_user.is_editor:
        raise HTTPException(
            status_code=400, detail="The user cannot be an editorial user."
        )

    # Obtener la cuenta del usuario actual
    account = session.get(Account, current_user.account.id)

    count_statement = select(func.count()).select_from(Review).where(Review.account_id == account.id)
    count = session.exec(count_statement).one()

    statement = select(Review).where(Review.account_id == account.id).offset(skip).limit(limit)
    reviews = session.exec(statement).all()

    reviews_out = [crud.review.convert_review_reviewOut(review=review) for review in reviews]

    return ReviewsOut(data=reviews_out, count=count)

@router.get("/{book_id}", response_model=ReviewsOut)
def read_all_reviews_by_book(session: SessionDep, book_id: uuid.UUID, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all reviews a specific book by ID.
    """

    count_statement = select(func.count()).select_from(Review).where(Review.book_id == book_id)
    count = session.exec(count_statement).one()

    statement = select(Review).where(Review.book_id == book_id).offset(skip).limit(limit)
    reviews = session.exec(statement).all()

    reviews_out = [crud.review.convert_review_reviewOut(review=review) for review in reviews]

    return ReviewsOut(data=reviews_out, count=count)


@router.get("/{review_id}", response_model=ReviewsOut)
def read_all_comments_by_review(session: SessionDep, review_id: uuid.UUID, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all commnts a specific review by ID.
    """
    # Obtener el número total de libros del usuario
    count_statement = select(func.count()).select_from(Comment).where(Comment.review_id == review_id)
    count = session.exec(count_statement).one()

    # Obtener los libros del usuario
    statement = select(Comment).where(Comment.review_id == review_id).offset(skip).limit(limit)
    comments = session.exec(statement).all()

    return CommentsOut(data=comments, count=count)



@router.get("/{book_id}", response_model=ReviewsOut)
def read_all_comment_by_book(session: SessionDep, book_id: uuid.UUID, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all comments a specific book by ID.
    """

    statement = select(Review).where(Review.book_id == book_id).offset(skip).limit(limit)
    reviews = session.exec(statement).all()

    count = 0
    comments = []
    for review in reviews:
        count_statement = select(func.count()).select_from(Comment).where(Comment.review_id == review.id)
        count += session.exec(count_statement).one()

        statement = select(Comment).where(Comment.review_id == review.id).offset(skip).limit(limit)
        comments.extend(session.exec(statement).all())

    return CommentsOut(data=comments, count=count)


@router.get("/{review_id}", response_model=ReviewOut)
def read_review_by_id(session: SessionDep, review_id: uuid.UUID):
    """
    Get a specific book by ID.
    """
    statement = select(Review).where(Review.id == review_id)
    review = session.exec(statement).first()

    if not review:
        raise HTTPException(
            status_code=404, detail="Review not found."  # Cambié el código de error a 404, ya que no se encuentra el libro.
        )
    review_out = crud.review.convert_review_reviewOut(review=review)

    return review_out


@router.post("/{book_id}", response_model=ReviewOut)
async def create_review_point_book(*, session: SessionDep, current_user: CurrentUser, review: ReviewCreatePointBook, book_id: uuid.UUID) -> Any:
    """
    Create new review with point book.
    """
    if current_user.is_editor:
        raise HTTPException(
            status_code=400, detail="The user cannot be an editorial user."
        )
    statement = select(Review).where((Review.book_id == book_id) & (Review.account_id == current_user.account.id))
    db_review = session.exec(statement).first()
    if db_review:
        raise HTTPException(
            status_code=400, detail="Review already exists."
        )

    book = crud.book.read_book_by_id(session=session, id=book_id)
    db_obj = crud.review.create_review_pb(session=session, review=review, book=book, current_user=current_user)
    # new_num_review es una variable per saber si hi ha +1, 0, -1, reviews en el book. (post, update, delete), en aquest cas +1
    crud.review.update_rating(session=session, book=book, new_num_review=1)

    review_out = crud.review.convert_review_reviewOut(review=db_obj)

    return review_out


@router.patch("/{book_id}", response_model=ReviewOut)
async def update_review_point_book(*, session: SessionDep, current_user: CurrentUser, review: ReviewUpdatePointBook, book_id: uuid.UUID) -> Any:
    """
    Update pointBook review.
    """
    if current_user.is_editor:
        raise HTTPException(
            status_code=400, detail="The user cannot be an editorial user."
        )
    statement = select(Review).where((Review.book_id == book_id) & (Review.account_id == current_user.account.id))
    db_review = session.exec(statement).first()
    if not db_review:
        raise HTTPException(
            status_code=400, detail="Review not found."
        )

    book = crud.book.read_book_by_id(session=session, id=book_id)
    db_obj = crud.review.update_point_book(session=session, review_in=review, db_review=db_review)
    # num_mew_review es una variable per saber si en el update, hi ha +1, 0, -1, book. (post, update, delete), en aquest cas 0
    crud.review.update_rating(session=session, book=book, new_num_review=0)

    review_out = crud.review.convert_review_reviewOut(review=db_obj)

    return review_out


@router.put("/{book_id}", response_model=ReviewOut)
async def update_or_create_review_point_book(*, session: SessionDep, current_user: CurrentUser, review: ReviewUpdatePointBook, book_id: uuid.UUID) -> Any:
    """
    Update pointBook review, if it does not exist it is created (Si s'ha creat la review a partir d'un Comment, PB es None i s'actualitza)
    """
    if current_user.is_editor:
        raise HTTPException(
            status_code=400, detail="The user cannot be an editorial user."
        )
    statement = select(Review).where((Review.book_id == book_id) & (Review.account_id == current_user.account.id))
    db_review = session.exec(statement).first()
    book = crud.book.read_book_by_id(session=session, id=book_id)
    if not db_review:
        db_obj = crud.review.create_review_pb(session=session, review=review, book=book, current_user=current_user)
        # new_num_review es una variable per saber si hi ha +1, 0, -1, reviews en el book. (post, update, delete), en aquest cas +1
        new_num_review = 1
    else:
        db_obj = crud.review.update_point_book(session=session, review_in=review, db_review=db_review)
        # num_mew_review es una variable per saber si en el update, hi ha +1, 0, -1, book. (post, update, delete), en aquest cas 0
        new_num_review = 0

    crud.review.update_rating(session=session, book=book, new_num_review=new_num_review)
    review_out = crud.review.convert_review_reviewOut(review=db_obj)

    return review_out


@router.patch("/{book_id}")
async def delete_review_point_book(*, session: SessionDep, current_user: CurrentUser, review: ReviewUpdatePointBook, book_id: uuid.UUID) -> Any:
    """
    Delete pointBook review. (La Review no se elimina si hay comments, sino si)
    """
    if current_user.is_editor:
        raise HTTPException(
            status_code=400, detail="The user cannot be an editorial user."
        )
    statement = select(Review).where((Review.book_id == book_id) & (Review.account_id == current_user.account.id))
    db_review = session.exec(statement).first()
    if not db_review:
        raise HTTPException(
            status_code=400, detail="Review not found."
        )

    book = crud.book.read_book_by_id(session=session, id=book_id)
    db_obj = crud.review.delete_point_book(session=session, db_review=db_review)
    # num_mew_review es una variable per saber si en el update, hi ha +1, 0, -1, book. (post, update, delete), en aquest cas 0
    crud.review.update_rating(session=session, book=book, new_num_review=-1)

    if not crud.review.there_are_comments(review=db_obj):
        crud.review.delete_review(session=session, db_review=db_review)
        return Message(message="Review deleted successfully")

    return Message(message="Point book deleted successfully")


"""
---------------------------------------------------------------------------------------------
"""

@router.post("/{book_id}", response_model=ReviewOut)
async def create_review_comment(*, session: SessionDep, current_user: CurrentUser, review: ReviewCreateComment, book_id: uuid.UUID) -> Any:
    """
    Create new review with comment.
    """
    if current_user.is_editor:
        raise HTTPException(
            status_code=400, detail="The user cannot be an editorial user."
        )
    statement = select(Review).where((Review.book_id == book_id) & (Review.account_id == current_user.account.id))
    db_review = session.exec(statement).first()
    if db_review:
        raise HTTPException(
            status_code=400, detail="Review already exists."
        )

    book = crud.book.read_book_by_id(session=session, id=book_id)

    db_obj = crud.review.create_review_empty(session=session, book=book, current_user=current_user)
    db_obj = crud.review.add_comment(session=session, review_in=review, db_review=db_obj)

    review_out = crud.review.convert_review_reviewOut(review=db_obj)

    return review_out


@router.post("/{book_id}", response_model=CommentOut)
async def add_comment_to_book(*, session: SessionDep, current_user: CurrentUser, review: ReviewCreateComment, book_id: uuid.UUID) -> Any:
    """
    add new comment to book.
    """
    if current_user.is_editor:
        raise HTTPException(
            status_code=400, detail="The user cannot be an editorial user."
        )
    statement = select(Review).where((Review.book_id == book_id) & (Review.account_id == current_user.account.id))
    db_review = session.exec(statement).first()
    if not db_review:
        raise HTTPException(
            status_code=400, detail="Review not found."
        )

    db_obj = crud.review.add_comment(session=session, review_in=review, db_review=db_review)

    review_out = crud.review.convert_review_reviewOut(review=db_obj)

    return review_out

@router.patch("/{book_id}/{comment_id}", response_model=CommentOut)
async def update_review_comment(*, session: SessionDep, current_user: CurrentUser, review: ReviewUpdateComment, book_id: uuid.UUID, comment_id: uuid.UUID) -> Any:
    """
    Update comment review.
    """
    if current_user.is_editor:
        raise HTTPException(
            status_code=400, detail="The user cannot be an editorial user."
        )
    statement = select(Review).where((Review.book_id == book_id) & (Review.account_id == current_user.account.id))
    db_review = session.exec(statement).first()
    if not db_review:
        raise HTTPException(
            status_code=400, detail="Review not found."
        )
    statement = select(Comment).where(Comment.id == comment_id)
    db_comment = session.exec(statement).first()
    if not db_comment:
        raise HTTPException(
            status_code=400, detail="Comment not found."
        )

    db_obj = crud.review.update_comment(session=session, comment=review, db_comment=db_comment)

    return db_obj


@router.put("/{book_id}", response_model=ReviewOut)
async def add_comment_or_create_review(*, session: SessionDep, current_user: CurrentUser, review: ReviewUpdatePointBook, book_id: uuid.UUID) -> Any:
    """
    Add comment review, if it does not exist it is created (Si s'ha creat la review a partir d'un PB, no hi ha comments i afegim a la review existen)
    """
    if current_user.is_editor:
        raise HTTPException(
            status_code=400, detail="The user cannot be an editorial user."
        )
    statement = select(Review).where((Review.book_id == book_id) & (Review.account_id == current_user.account.id))
    db_review = session.exec(statement).first()
    book = crud.book.read_book_by_id(session=session, id=book_id)
    if not db_review:
        db_review = crud.review.create_review_empty(session=session, book=book, current_user=current_user)

    db_obj = crud.review.add_comment(session=session, review_in=review, db_review=db_review)
    review_out = crud.review.convert_review_reviewOut(review=db_obj)

    return review_out


@router.patch("/{book_id}/{comment_id}")
async def delete_comment(*, session: SessionDep, current_user: CurrentUser, comment_id: uuid.UUID, book_id: uuid.UUID) -> Any:
    """
    Delete comment review. (La Review no se elimina, a no ser que point book sea None y no queden más comments)
    """
    if current_user.is_editor:
        raise HTTPException(
            status_code=400, detail="The user cannot be an editorial user."
        )
    statement = select(Review).where((Review.book_id == book_id) & (Review.account_id == current_user.account.id))
    db_review = session.exec(statement).first()
    if not db_review:
        raise HTTPException(
            status_code=400, detail="Review not found."
        )

    db_review = crud.review.delete_comment(session=session, db_review=db_review, comment_id=comment_id)
    # num_mew_review es una variable per saber si en el update, hi ha +1, 0, -1, book. (post, update, delete), en aquest cas 0

    if not crud.review.there_are_comments(review=db_review) and not crud.review.is_point_book(review=db_review):
        crud.review.delete_review(session=session, db_review=db_review)
        return Message(message="Review deleted successfully")

    return Message(message="Comment deleted successfully")