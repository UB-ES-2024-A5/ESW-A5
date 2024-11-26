""" Account related CRUD methods """
from typing import Any

from sqlmodel import Session, select

from fastapi import HTTPException

from app.models import Account, AccountCreate, AccountUpdate
import uuid

def create_account(session: Session, account: AccountCreate) -> Account:
    db_obj = Account(
        id=account.id,
        photo=account.photo,
        bio=account.bio,
        num_followers=0,
        num_following=0
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

def get_account_by_id(*, session: Session, id: uuid.UUID) -> Account | None:
    statement = select(Account).where(Account.id == id)
    session_account = session.exec(statement).first()
    return session_account