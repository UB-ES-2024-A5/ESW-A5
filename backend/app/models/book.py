""" Book models """
import uuid
from typing import List

from sqlmodel import Field, Relationship
from .base import SQLModel
from .wishlist_book_link import WishlistBookLink


# Shared properties
class BookBase(SQLModel):
    title: str = Field(index=True, max_length=255)
    author: str = Field(index=True, max_length=255)
    gender_main: str  # Es obligatori un genere pero no dos
    gender_secondary: str | None = None
    synopsis: str | None = None
    publication_year: int | None = None
    isbn: str | None = Field(unique=True, index=True, min_length=10, max_length=13)  #El ISBN es compon de 13 numeros, pero existeixen de 10
    price: float | None = None
    img: str | None = None


# Database model, database table inferred from class name
class Book(BookBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    rating: float = 0.0
    account_id: uuid.UUID = Field(foreign_key="account.id")
    account: "Account" = Relationship(back_populates="books")
    links: List["Link"] = Relationship(back_populates="book")

    wishlists: List["WishList"] = Relationship(back_populates="books", link_model=WishlistBookLink)


class BookOut(BookBase):
    id: uuid.UUID
    list_links: List['str']


class BooksOut(SQLModel):
    data: list[BookOut]
    count: int

# Són els únics atributs que es poden modificar
class BookUpdate(SQLModel):
    synopsis: str | None = None
    price: float | None = None
    img: str | None = None
    links: List[str]

class BookUpdateSuper(SQLModel):
    title: str
    author: str
    gender_main: str  # Es obligatori un genere pero no dos
    gender_secondary: str | None = None
    synopsis: str | None = None
    publication_year: int
    price: float | None = None
    img: str | None = None
    links: List[str]


# Modelo para la creación de un libro, donde incluimos la lista de enlaces
class BookCreate(BookBase):
    links: List[str]  # Lista de enlaces para el libro