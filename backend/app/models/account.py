""" User accounts model class """
import uuid

from .base import SQLModel
from sqlmodel import Field, Relationship
from typing import List

class AccountBase(SQLModel):
    id: uuid.UUID = Field(default=None, primary_key=True, foreign_key="user.id")
    photo: str | None = None
    bio: str | None = Field(default=None, max_length=200)

class Account(AccountBase, table=True):
    user: "User" = Relationship(back_populates="account")

class AccountUpdate(AccountBase):
    pass

class AccountCreate(AccountBase):
    pass

class AccountOut(AccountBase):
    pass

class AccountsOut(SQLModel):
    data: List[AccountOut]
    count: int