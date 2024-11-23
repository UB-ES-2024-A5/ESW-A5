""" Follower models """
import uuid

from .base import SQLModel
from .wishlist_book_link import WishlistBookLink
from sqlmodel import Field, Relationship
from typing import List


class FollowerBase(SQLModel):
    pass


class Follower(FollowerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # ID de la cuenta que sigue
    follower_id: uuid.UUID = Field(foreign_key="account.id", ondelete="CASCADE")
    # ID de la cuenta que es seguida
    following_id: uuid.UUID = Field(foreign_key="account.id", ondelete="CASCADE")
    # Relación con la cuenta que sigue
    follower_account: "Account" = Relationship(back_populates="following")
    # Relación con la cuenta que es seguida
    following_account: "Account" = Relationship(back_populates="followers")


class FollowerCreate(FollowerBase):
    pass


class FollowerUpdate(FollowerBase):
    pass


class FollowerOut(FollowerBase):
    id: uuid.UUID


class FollowersOut(SQLModel):
    data: List[FollowerOut]
    count: int
