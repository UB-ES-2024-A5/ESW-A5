import uuid

from .base import SQLModel
from .wishlist_book_link import WishlistBookLink
from sqlmodel import Field, Relationship
from typing import List

class WishListBase(SQLModel):
    name: str | None = Field(default=None)
    icon: str | None = Field(default=None)
    description: str | None = Field(default=None)
class WishList(WishListBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    account_id: uuid.UUID = Field(foreign_key="account.id")
    account: "Account" = Relationship(back_populates="wishlists")

    books: List["Book"] = Relationship(back_populates="wishlists", link_model=WishlistBookLink)

class WishListCreate(WishListBase):
    pass

class WishListUpdate(WishListBase):
    pass

class WishListOut(WishListBase):
    id: uuid.UUID

class WishListsOut(SQLModel):
    data: List[WishListOut]
    count: int





