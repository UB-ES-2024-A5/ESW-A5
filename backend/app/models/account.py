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
    books: List["Book"] = Relationship(back_populates="account")
    wishlists: List["WishList"] = Relationship(back_populates="account")
    reviews: List["Review"] = Relationship(back_populates="account")
    # El cascade sirve para assegurar que si una cuenta es eliminada, todos los Follower relacionados con esta cuenta se elimina
    following: List["Follower"] = Relationship(
        back_populates="following_account",
        sa_relationship_kwargs={"cascade": "all, delete", "foreign_keys": "Follower.following_id"}    )
    followers: List["Follower"] = Relationship(
        back_populates="followers_account",
        sa_relationship_kwargs={"cascade": "all, delete", "foreign_keys": "Follower.follower_id"}
   )

class AccountUpdate(SQLModel):
    photo: str | None = None
    bio: str | None = Field(default=None, max_length=200)

class AccountUpdateMe(SQLModel):
    photo: str | None = None
    bio: str | None = Field(default=None, max_length=200)

class AccountCreate(AccountBase):
    pass

class AccountOut(AccountBase):
    pass

class AccountsOut(SQLModel):
    data: List[AccountOut]
    count: int