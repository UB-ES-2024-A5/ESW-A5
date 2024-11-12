""" Books management routes """

import uuid

from typing import Any

from sqlmodel import col, delete, func, select
from fastapi import APIRouter, Depends, HTTPException

from app import crud
from app.api.deps import (
    CurrentUser, SessionDep, get_current_active_superuser,
)

from app.models import (
    Book, BookCreate, BookUpdate, BookOut, BooksOut, BookUpdateSuper, User, Message, Account, Link, LinksOut
)

router = APIRouter()


@router.get("/", response_model=BooksOut)
def read_all_books(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all books.
    """
    count_statement = select(func.count()).select_from(Book)
    count = session.exec(count_statement).one()

    statement = select(Book).offset(skip).limit(limit)
    books = session.exec(statement).all()

    # Esto es necessario para cnvertir los Book, en BookOut donde contiene una lista de strings con url de los links
    books_out = [crud.book.convert_book_bookOut(book=book) for book in books]

    return BooksOut(data=books_out, count=count)


@router.get("/search_id/{book_id}", response_model=BookOut)
def read_book_by_id(session: SessionDep, book_id: uuid.UUID):
    """
    Get a specific book by ID.
    """
    statement = select(Book).where(Book.id == book_id)
    book = session.exec(statement).first()

    if not book:
        raise HTTPException(
            status_code=404, detail="Book not found."  # Cambié el código de error a 404, ya que no se encuentra el libro.
        )
    book_out = crud.book.convert_book_bookOut(book=book)

    return book_out


@router.get("/links/{book_id}", response_model=LinksOut)
def read_links_by_idBook(session: SessionDep, book_id: uuid.UUID, skip: int = 0, limit: int = 100) -> Any:
    """
    Get links by Book ID.
    """
    statement = select(Book).where(Book.id == book_id)
    book = session.exec(statement).first()

    if not book:
        raise HTTPException(
            status_code=404, detail="Book not found."  # Cambié el código de error a 404, ya que no se encuentra el libro.
        )

    count_statement = select(func.count()).select_from(Link).where(Link.book_id == book_id)
    count = session.exec(count_statement).one()

    statement = select(Link).where(Link.book_id == book_id).offset(skip).limit(limit)
    links = session.exec(statement).all()

    return LinksOut(data=links, count=count)

@router.get("/my_books", response_model=BooksOut)
def read_all_my_books(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all books for the current user, editorial user only.
    """
    if not current_user.is_editor:
        raise HTTPException(
            status_code=400, detail="User must be an editorial user."
        )

    # Obtener la cuenta del usuario actual
    account = session.get(Account, current_user.account.id)

    # Obtener el número total de libros del usuario
    count_statement = select(func.count()).select_from(Book).where(Book.account_id == account.id)
    count = session.exec(count_statement).one()

    # Obtener los libros del usuario
    statement = select(Book).where(Book.account_id == account.id).offset(skip).limit(limit)
    books = session.exec(statement).all()

    books_out = [crud.book.convert_book_bookOut(book=book) for book in books]

    return BooksOut(data=books_out, count=count)



@router.post("/", response_model=BookOut)
async def create_book(*, session: SessionDep, current_user: CurrentUser, book: BookCreate):
    """
    Create/Publisher new book.
    """
    if not current_user.is_editor:
        raise HTTPException(
            status_code=400, detail="User must be an editorial user."
        )
    statement = select(Book).where(Book.isbn == book.isbn)
    db_book = session.exec(statement).first()
    if db_book:
        raise HTTPException(
            status_code=400, detail="Book already exists."
        )
    if crud.book.is_link_in_db(session=session, links=book.links):
        raise HTTPException(
            status_code=400, detail="The links are already being used in another book."
        )

    db_obj = crud.book.create_book(session=session, book=book, current_user=current_user)
    db_obj = crud.book.add_links(session=session, book=book, db_obj=db_obj)

    book_out = crud.book.convert_book_bookOut(book=db_obj)

    return book_out

@router.patch("/superUser/{book_id}", dependencies=[Depends(get_current_active_superuser)], response_model=BookOut)
def updateSuper_book(*, session: SessionDep, book_id: uuid.UUID, book_in: BookUpdateSuper) -> Any:
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(
            status_code=404,
            detail="The Book with this id does not exist in the system",
        )

    db_book = crud.book.update_book(session=session, db_book=db_book, book_in=book_in)
    book_out = crud.book.convert_book_bookOut(book=db_book)
    return book_out

@router.patch("/{book_id}", response_model=BookOut)
def update_book(*, session: SessionDep, book_id: uuid.UUID, current_user: CurrentUser, book_in: BookUpdate) -> Any:
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(
            status_code=404,
            detail="The Book with this id does not exist in the system",
        )
    if not current_user.is_editor:
        raise HTTPException(
            status_code=400,
            detail="User must be an editorial user."
        )
    if not (db_book.account_id == current_user.account.id):
        raise HTTPException(
            status_code=400,
            detail="This book does not belong to your user."
        )

    db_book = crud.book.update_book(session=session, db_book=db_book, book_in=book_in)
    book_out = crud.book.convert_book_bookOut(book=db_book)
    return book_out
@router.delete("/{book_id}")
def delete_book(session: SessionDep, current_user: CurrentUser, book_id: uuid.UUID) -> Message:
   
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    elif not current_user.is_editor:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    elif not (current_user.account.id == book.account_id):
        raise HTTPException(
            status_code=403, detail="This book does not belong to your user"
        )
    for link in book.links:
        session.delete(link)
    session.delete(book)
    session.commit()
    return Message(message="Book deleted successfully")
