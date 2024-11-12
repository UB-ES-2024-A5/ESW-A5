""" Wishlist related CRUD methods """
from typing import Any

from sqlmodel import Session, select

from fastapi import HTTPException

from app.models import WishList, WishListCreate, WishListUpdate

def create_wishlist(session: Session, account: WishListCreate) -> WishList:
    db_obj = WishList(

    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

#def update_wishlist(*, session: Session, db_account: Account, account_in: AccountUpdate) -> Any:
 #   account_data = account_in.model_dump(exclude_unset=True)
  #  db_account.sqlmodel_update(account_data)
   # session.add(db_account)
    #session.commit()
    #session.refresh(db_account)
    #return db_account