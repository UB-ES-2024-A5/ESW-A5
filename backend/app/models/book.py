""" Book models """
import uuid

from sqlmodel import Field, Relationship
from .base import SQLModel


# Shared properties
class BookBase(SQLModel):
    title: str = Field(index=True, max_length=255)
    author: str = Field(index=True, max_length=255)
    gender_main: str  # Es obligatori un genere pero no dos
    gender_secondary: str | None = None
    synopsis: float | None = None
    publication_year: int | None = None
    isbn: int | None = Field(unique=True, index=True, min_length=10, max_length=13)  #El ISBN es compon de 13 numeros, pero existeixen de 10
    price: int | None = None
    img: str | None = None


# Database model, database table inferred from class name
class Book(BookBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    account_id: int = Field(foreign_key="account.id")
    account: "Account" = Relationship(back_populates="book")
    links: list["Link"] = Relationship(back_populates="book")


class BookOut(BookBase):
    id: int

class BooksOut(SQLModel):
    data: list[BookOut]
    count: int

# Són els únics atributs que es poden modificar
class BookUpdate(BookBase):
    synopsis: float | None = None
    price: int | None = None
    img: str | None = None
    links: list["Link"]

# Modelo para la creación de un libro, donde incluimos la lista de enlaces
class BookCreate(BookBase):
    links: list["Link"]  # Lista de enlaces para el libro