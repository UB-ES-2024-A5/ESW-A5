""" Wishlists management routes """
import uuid

from typing import Any

from sqlmodel import col, delete, func, select

from fastapi import APIRouter, Depends, HTTPException

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)

from app.models import (
    WishList,
    WishListCreate,
    WishListUpdate,
    WishListOut,
    WishListsOut,
    WishlistBookLink,
    User,
    Account,
    Book,
    BooksOut,
    Message
)

router = APIRouter()

@router.post(
    "/",
    response_model=WishList
)
def create_wishlist(*, session: SessionDep, current_user: CurrentUser, wishlist: WishListCreate) -> Any:
    """
    Create new empty wishlist.
    """
    db_obj = crud.wishlist.create_wishlist(session=session, wishlist=wishlist, current_user=current_user)

    return db_obj

@router.get("/", response_model=WishListsOut)
def read_wishlists(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all wishlists.
    """
    count_statement = select(func.count()).select_from(WishList)
    count = session.exec(count_statement).one()

    statement = select(WishList).offset(skip).limit(limit)
    wishlists = session.exec(statement).all()

    return WishListsOut(data=wishlists, count=count)


@router.get("/me", response_model=WishListsOut)
def read_wishlists_me(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all wishlists for the current user
    """

    # Obtener la cuenta del usuario actual
    account = session.get(Account, current_user.account.id)

    # Obtener el número total de wishlists de la cuenta
    count_statement = select(func.count()).select_from(WishList).where(WishList.account_id == account.id)
    count = session.exec(count_statement).one()

    # Obtener las wishlists de la cuenta
    statement = select(WishList).where(WishList.account_id == account.id).offset(skip).limit(limit)
    wishlists = session.exec(statement).all()

    return WishListsOut(data=wishlists, count=count)

@router.get("/{wishlist_id}",
            dependencies=[Depends(get_current_active_superuser)],
            response_model=WishListOut)
def read_wishlist_by_id(session: SessionDep, wishlist_id: uuid.UUID):
    """
    Get a specific wishlist by ID.
    """
    statement = select(WishList).where(WishList.id == wishlist_id)
    wishlist = session.exec(statement).first()

    if not wishlist:
        raise HTTPException(
            status_code=404, detail="WishList not found."  # Cambié el código de error a 404, ya que no se encuentra el libro.
        )

    return wishlist

@router.get("/{wishlist_id}/books", response_model=BooksOut)
def read_books_from_wishlist(session: SessionDep, wishlist_id: uuid.UUID) -> Any:
    """
    Get all books for given wishlist.
    """

    # Obtener el número total de books de la wishlist
    count_statement = select(func.count()).select_from(WishlistBookLink).where(WishlistBookLink.wishlist_id == wishlist_id)
    count = session.exec(count_statement).one()

    # Obtener los book_links de la wishlist
    statement = (
        select(Book)
        .join(WishlistBookLink, WishlistBookLink.book_id == Book.id)
        .where(WishlistBookLink.wishlist_id == wishlist_id)
    )
    books = session.exec(statement).all()

    books_out = [crud.book.convert_book_bookOut(book=book) for book in books]

    return BooksOut(data=books_out, count=count)

@router.patch(
    "/{wishlist_id}",
    response_model=WishListOut,
)
def update_wishlist(
        *,
        session: SessionDep,
        wishlist_id: uuid.UUID,
        wishlist_in: WishListUpdate,
) -> Any:
    """
    Update a specific wishlist.
    """

    db_wishlist = session.get(WishList, wishlist_id)
    if not db_wishlist:
        raise HTTPException(
            status_code=404,
            detail="The wishlist with this id does not exist in the system",
        )

    db_wishlist = crud.wishlist.update_wishlist(session=session, db_wishlist=db_wishlist, wishlist_in=wishlist_in)
    return db_wishlist

@router.patch(
    "/{wishlist_id}/{book_id}",
    response_model=Message,
)
def add_book_to_wishlist(
        *,
        session: SessionDep,
        wishlist_id: uuid.UUID,
        book_id: uuid.UUID,
) -> Any:
    """
    Add a specific book to specific wishlist.
    """

    db_wishlist = session.get(WishList, wishlist_id)
    if not db_wishlist:
        raise HTTPException(
            status_code=404,
            detail="The wishlist with this id does not exist in the system",
        )

    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(
            status_code=404,
            detail="The book with this id does not exist in the system",
        )

    # Verificar si el libro ya está en la wishlist
    existing_link = session.query(WishlistBookLink).filter_by(
        wishlist_id=wishlist_id, book_id=book_id
    ).first()

    if existing_link:
        raise HTTPException(
            status_code=400,
            detail="Book already added to wishlist"
        )

    # Crear un nuevo enlace entre el libro y la wishlist
    new_link = WishlistBookLink(
        wishlist_id=wishlist_id,
        book_id=book_id
    )
    session.add(new_link)
    session.commit()
    session.refresh(new_link)

    # Ahora, devolvemos la wishlist con los libros actualizados
    return Message(message="Book added correctly")


