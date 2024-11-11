""" Account related CRUD methods """
from typing import Any

from sqlmodel import Session, select

from fastapi import HTTPException

from app.models import Account, AccountCreate, AccountUpdate

def create_account(session: Session, account: AccountCreate) -> Account:
    db_obj = Account(
        id=account.id,
        photo=account.photo,
        bio=account.bio
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_account(*, session: Session, db_account: Account, account_in: AccountUpdate) -> Any:
    account_data = account_in.model_dump(exclude_unset=True)
    db_account.sqlmodel_update(account_data)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account