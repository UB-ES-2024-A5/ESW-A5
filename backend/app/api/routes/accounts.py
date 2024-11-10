""" Accounts management routes """
import uuid

from typing import Any

from sqlmodel import col, delete, func, select

from fastapi import APIRouter, Depends, HTTPException

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)

from app.models import (
    Account,
    AccountCreate,
    AccountUpdate,
    AccountOut,
    AccountsOut,
    User
)

router = APIRouter()


@router.get("/me", response_model=AccountOut)
def read_account_me(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Get current account.
    """
    account = session.get(Account, current_user.id)

    return account

@router.get("/{account_id}",
            response_model=AccountOut,
            dependencies=[Depends(get_current_active_superuser)])
def read_account_by_id(
        account_id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Get a specific account by ID (must be need superuser).
    """
    account = session.get(Account, account_id)

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )

    return account

@router.get(
    "/",
    response_model=AccountsOut
)
def read_accounts(session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve accounts.
    """

    count_statement = select(func.count()).select_from(Account)
    count = session.exec(count_statement).one()

    statement = select(Account).offset(skip).limit(limit)
    accounts = session.exec(statement).all()

    return AccountsOut(data=accounts, count=count)

@router.post(
    "/",
    response_model=Account
)
async def create_account(*, session: SessionDep, account: AccountCreate) -> Any:
    """
    Create new account.
    """
    db_account = session.get(Account, account.id)
    user = session.get(User, account.id)

    if db_account:
        raise HTTPException(
            status_code=400, detail="Account already exists."
        )

    if not user:
        raise HTTPException(
            status_code=400, detail="User does not exist."
        )

    db_obj = crud.account.create_account(session=session, account=account)

    return db_obj
