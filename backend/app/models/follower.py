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
    # ID de la cuenta que empieza a seguir (current_user)
    follower_id: uuid.UUID = Field(foreign_key="account.id")
    # ID de la cuenta que es seguida (a quien quiero seguir)
    following_id: uuid.UUID = Field(foreign_key="account.id")
    # Relación con la cuenta que empieza a seguir
    followers_account: "Account" = Relationship(
        back_populates="following",
        sa_relationship_kwargs={"foreign_keys": "Follower.follower_id"}
    )
    # Relación con la cuenta que es seguida
    following_account: "Account" = Relationship(
        back_populates="followers",
        sa_relationship_kwargs={"foreign_keys": "Follower.following_id"}
    )


class FollowerCreate(FollowerBase):
    pass


class FollowerUpdate(FollowerBase):
    pass


class FollowerOut(FollowerBase):
    id: uuid.UUID
    follower_id: uuid.UUID
    following_id: uuid.UUID


class FollowersOut(SQLModel):
    data: List[FollowerOut]
    count: int
