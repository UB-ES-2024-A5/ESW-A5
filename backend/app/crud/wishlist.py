""" Wishlist related CRUD methods """
from typing import Any

from sqlmodel import Session, select

from fastapi import HTTPException

from app.models import WishList, WishListCreate, WishListUpdate, User

def create_wishlist(session: Session, wishlist: WishListCreate, current_user: User) -> WishList:
    db_obj = WishList(
        name=wishlist.name,
        icon=wishlist.icon,
        description=wishlist.description,
        account_id=current_user.account.id
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_wishlist(*, session: Session, db_wishlist: WishList, wishlist_in: WishListUpdate) -> Any:
    wishlist_data = wishlist_in.model_dump(exclude_unset=True)
    db_wishlist.sqlmodel_update(wishlist_data)
    session.add(db_wishlist)
    session.commit()
    session.refresh(db_wishlist)
    return db_wishlist