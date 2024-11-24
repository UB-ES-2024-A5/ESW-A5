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
    follower_id: uuid.UUID = Field(foreign_key="account.id")
    # ID de la cuenta que es seguida
    following_id: uuid.UUID = Field(foreign_key="account.id")
    # Relación con la cuenta que sigue
    follower_account: "Account" = Relationship(
        back_populates="following",
        sa_relationship_kwargs=dict(foreign_keys="Follower.follower_id")
    )
    # Relación con la cuenta que es seguida
    following_account: "Account" = Relationship(
        back_populates="followers",
        sa_relationship_kwargs=dict(foreign_keys="Follower.following_id")
    )


class FollowerCreate(FollowerBase):
    pass


class FollowerUpdate(FollowerBase):
    pass


class FollowerOut(FollowerBase):
    id: uuid.UUID


class FollowersOut(SQLModel):
    data: List[FollowerOut]
    count: int
