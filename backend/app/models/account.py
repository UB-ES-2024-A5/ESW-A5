""" User accounts model class """
import uuid

from . import User
from .base import SQLModel
from sqlmodel import Field, Relationship
from typing import List

from .book import Book


class AccountBase(SQLModel):
    photo: str | None = None
    bio: str | None = None

class Account(AccountBase, table=True):
    id: uuid.UUID = Field(default=None, primary_key=True, foreign_key="user.id")

    user: "User" = Relationship(back_populates="account")
    books: List["Book"] = Relationship(back_populates="account")

class AccountOut(AccountBase):
    id: uuid.UUID

class AccountsOut(SQLModel):
    data: List[AccountOut]
    count: int