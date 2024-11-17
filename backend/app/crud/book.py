""" Book related CRUD methods """

from typing import Any, List

from sqlmodel import Session, select
from fastapi import HTTPException
from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate, UserUpdate, Link, Book, BookCreate, BookUpdate, BookUpdateSuper, BookOut
import uuid

def create_book(session: Session, book: BookCreate, current_user: User) -> Book:
    db_obj = Book(
        title=book.title,
        author=book.author,
        gender_main=book.gender_main,
        gender_secondary=book.gender_secondary,
        synopsis=book.synopsis,
        publication_year=book.publication_year,
        isbn=book.isbn,
        price=book.price,
        img=book.img,
        account_id=current_user.account.id
    )
    current_user.account.books.append(db_obj)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def is_link_in_db(session: Session, links: List[str]):
    """
    Check if the links already exist.
    """
    # Obtener los enlaces existentes para este libro
    for url in links:
        existing_link = session.query(Link).filter(Link.url == url).first()
        if existing_link:
            return True
    return False

def add_links(session: Session, book: BookCreate, db_obj: Book) -> Book:
    for links_data in book.links:
        link = Link(url=links_data)

        db_obj.links.append(link)
        session.add(link)

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_book(session: Session, db_book: Book, book_in: BookUpdateSuper) -> Book:
    book_info = book_in.model_dump(exclude_unset=True)
    db_book.sqlmodel_update(book_info)
    if "links" in book_info:
        new_links = {url for url in book_info["links"]}  # Lista de los links pasados en BookUpdateSuper
        current_links = {link.url for link in db_book.links}  # Lista de los links actuales
        links_to_delete = [link for link in db_book.links if link.url not in new_links]  # Links que estan en current y no en new
        links_to_add = new_links - current_links  # Links que estan en new y no estavan en current

        if is_link_in_db(session=session, links=links_to_add):
            raise HTTPException(
                status_code=404,
                detail="The Book with this id does not exist in the system",
            )

        for link in links_to_delete:  #Eliminamos links antiguos
            session.delete(link)

        for url in links_to_add:
            new_link = Link(url=url, book_id=db_book.id)
            db_book.links.append(new_link)
            session.add(new_link)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

def update_link(session: Session, db_link: Link, new_url: str) -> Link:
    db_link.url = new_url  # Actualizem la URL
    session.add(db_link)
    session.commit()
    session.refresh(db_link)
    return db_link


def convert_book_bookOut(book: Book):
    bookOut = BookOut(
        id=book.id,
        title=book.title,
        author=book.author,
        gender_main=book.gender_main,
        gender_secondary=book.gender_secondary,
        synopsis=book.synopsis,
        publication_year=book.publication_year,
        isbn=str(book.isbn),
        price=book.price,
        img=book.img,
        list_links=[link.url for link in book.links],  # Mapear los links como strings
        account_id=book.account_id
    )
    return bookOut

def read_book_by_id(session:Session, id: uuid.UUID) -> Book:
    statement = select(Book).where(Book.id == id)
    return session.exec(statement).first()