import uuid

from .base import SQLModel
from sqlmodel import Field, Relationship
from typing import List

class ReviewBase(SQLModel):
    point_book: int | None = Field(default=None)

class Review(ReviewBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    account_id: uuid.UUID = Field(foreign_key="account.id")
    account: "Account" = Relationship(back_populates="reviews")
    book_id: uuid.UUID = Field(foreign_key="book.id")
    book: "Book" = Relationship(back_populates="reviews")
    comments: List["Comment"] = Relationship(back_populates="review")

# Per crear review si no existeix la valoracio tant en comment com amb point
class ReviewCreatePointBook(SQLModel):
    point_book: int

class ReviewCreateComment(SQLModel):
    c: str

#Per modificar si canvia el point, i per afegir un altre comment
# Els comments no es poden editar nomes
class ReviewUpdatePointBook(ReviewCreatePointBook):
    pass

class ReviewUpdateComment(ReviewCreateComment):
    pass
class ReviewOut(ReviewBase):
    id: uuid.UUID
    list_comments: List[str]
class ReviewsOut(SQLModel):
    data: List[ReviewOut]
    count: int
