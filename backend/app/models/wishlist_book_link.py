import uuid

from sqlmodel import Field
from datetime import datetime
from .base import SQLModel
from .enums import StateEnum

class WishlistBookLink(SQLModel, table=True):
    wishlist_id: uuid.UUID | None = Field(default=None, foreign_key="wishlist.id", primary_key=True)
    book_id: uuid.UUID | None = Field(default=None, foreign_key="book.id", primary_key=True)
    added_date: datetime = Field(default=datetime.now())
    priority: int | None = Field(default=None)
    state: StateEnum = Field(default=StateEnum.PENDIENTE)
