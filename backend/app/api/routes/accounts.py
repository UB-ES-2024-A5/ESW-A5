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
    AccountUpdateMe,
    AccountOut,
    AccountsOut,
    User,
    Message
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
            response_model=AccountOut)
def read_account_by_id(
        account_id: uuid.UUID, session: SessionDep) -> Any:
    """
    Get a specific account by ID (must be need superuser).
    """
    account = session.get(Account, account_id)

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

@router.patch("/me", response_model=AccountOut)
def update_account_me(
        *, session: SessionDep, account_in: AccountUpdateMe, current_user: CurrentUser
) -> Any:
    """
    Update own account.
    """

    current_account = session.get(Account, current_user.id)
    account_data = account_in.model_dump(exclude_unset=True)
    current_account.sqlmodel_update(account_data)
    session.add(current_account)
    session.commit()
    session.refresh(current_account)
    return current_account

@router.patch(
    "/{account_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=AccountOut,
)
def update_account(
        *,
        session: SessionDep,
        account_id: uuid.UUID,
        account_in: AccountUpdate,
) -> Any:
    """
    Update an specific account.
    """

    db_account = session.get(Account, account_id)
    if not db_account:
        raise HTTPException(
            status_code=404,
            detail="The account with this id does not exist in the system",
        )

    db_account = crud.account.update_account(session=session, db_account=db_account, account_in=account_in)
    return db_account

@router.delete(
    "/me",
)
def delete_account_me(
        session: SessionDep, current_user: CurrentUser
) -> Message:
    """
    Delete own account.
    """
    account = session.get(Account, current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    elif current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )

    session.delete(account)
    session.commit()
    return Message(message="Account deleted successfully")

@router.delete(
    "/{account_id}",
    dependencies=[Depends(get_current_active_superuser)],)
def delete_account(
        session: SessionDep, current_user: CurrentUser, account_id: uuid.UUID
) -> Message:
    """
    Delete an account (must be need superuser).
    """
    account = session.get(Account, account_id)
    user = session.get(User, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    elif user != current_user and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    elif user == current_user and current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )

    session.delete(account)
    session.commit()
    return Message(message="Account deleted successfully")
