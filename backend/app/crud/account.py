""" Account related CRUD methods """
from sqlmodel import Session, select

from fastapi import HTTPException

from app.models import Account, AccountCreate

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