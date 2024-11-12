""" Link models """
import uuid

from sqlmodel import Field, Relationship
from .base import SQLModel

class LinkBase(SQLModel):
    url: str = Field(unique=True, max_length=255)

class Link(LinkBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    book_id: uuid.UUID = Field(foreign_key="book.id")
    book: "Book" = Relationship(back_populates="links")

class LinkOut(LinkBase):
    id: uuid.UUID

class LinksOut(SQLModel):
    data: list[LinkOut]
    count: int

class LinkUpdate(SQLModel):
    url: str

