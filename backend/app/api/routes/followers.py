""" Followers management routes """
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
    Follower,
    FollowerCreate,
    FollowerUpdate,
    FollowerOut,
    FollowersOut,
    WishlistBookLink,
    User,
    Account,
    Book,
    BooksOut,
    Message,
    AccountOut,
    AccountsOut
)

router = APIRouter()


@router.post("/{account_id}", response_model=FollowerOut)
def add_followed(*, session: SessionDep, current_user: CurrentUser, account_id: uuid.UUID) -> Any:
    """
    Create new follow.
    """
    statement = select(Account).where(Account.id == account_id)
    account = session.exec(statement).first()

    if not account:
        raise HTTPException(
            status_code=404, detail="Account not found."
        )
    if account == current_user.account:
        raise HTTPException(
            status_code=403, detail="You can't follow yourself."
        )

    statement = select(Follower).where(
        Follower.follower_id == current_user.account.id , Follower.following_id == account_id)
    follow = session.exec(statement).first()
    if follow:
        raise HTTPException(
            status_code=404, detail="Follower exist."
        )

    db_follow = crud.follower.create_follow(session=session, account=account, current_user=current_user)

    return db_follow


@router.delete("/{account_id}", response_model=Message)
def unfollow(*, session: SessionDep, current_user: CurrentUser, account_id: uuid.UUID) -> Any:
    """
    Delete a Follower - Unfollow.
    """
    statement = select(Account).where(Account.id == account_id)
    account = session.exec(statement).first()

    if not account:
        raise HTTPException(
            status_code=404, detail="Account not found."
        )

    statement = select(Follower).where(
        Follower.follower_id == current_user.account.id and Follower.following_id == account_id)
    follow = session.exec(statement).first()
    if not follow:
        raise HTTPException(
            status_code=404, detail="Follower not found."
        )

    crud.follower.delete_follow(session=session, account=account, current_user=current_user, follow=follow)

    return Message(message="Unfollow successfully")


@router.get("/me_followers", response_model=FollowersOut)
def read_all_me_followers(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all followers for the current user
    """

    # Obtener la cuenta del usuario actual
    account = session.get(Account, current_user.account.id)

    # Obtener el número total de followers de la cuenta
    count_statement = select(func.count()).select_from(Follower).where(Follower.following_id == account.id)
    count = session.exec(count_statement).one()

    # Obtener los followers de la cuenta
    statement = select(Follower).where(Follower.following_id == account.id).offset(skip).limit(limit)
    followers = session.exec(statement).all()

    return FollowersOut(data=followers, count=count)


@router.get("/me_following", response_model=FollowersOut)
def read_all_me_following(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all followings for the current user
    """

    # Obtener la cuenta del usuario actual
    account = session.get(Account, current_user.account.id)

    # Obtener el número total de follower de la cuenta
    count_statement = select(func.count()).select_from(Follower).where(Follower.follower_id == account.id)
    count = session.exec(count_statement).one()

    # Obtener las follower de la cuenta
    statement = select(Follower).where(Follower.follower_id == account.id).offset(skip).limit(limit)
    follower = session.exec(statement).all()

    return FollowersOut(data=follower, count=count)


@router.get("/me_followers_accounts", response_model=AccountsOut)
def read_all_me_followers_accounts(session: SessionDep, current_user: CurrentUser, skip: int = 0,
                                   limit: int = 1000) -> Any:
    """
    Get all followers for the current user
    """

    # Obtener la cuenta del usuario actual
    account = session.get(Account, current_user.account.id)

    # Obtener el número total de followers de la cuenta
    count_statement = select(func.count()).select_from(Account).join(
        Follower, Account.id == Follower.follower_id).where(Follower.following_id == account.id)
    count = session.exec(count_statement).one()

    # Obtener los followers de la cuenta
    statement = select(Account).join(Follower, Account.id == Follower.follower_id).where(
        Follower.following_id == account.id).offset(skip).limit(limit)
    accounts_out = session.exec(statement).all()

    return AccountsOut(data=accounts_out, count=count)


@router.get("/me_following_accounts", response_model=AccountsOut)
def read_all_me_following_accounts(session: SessionDep, current_user: CurrentUser, skip: int = 0,
                                   limit: int = 100) -> Any:
    """
    Get all accounts followings for the current user
    """

    # Obtener la cuenta del usuario actual
    account = session.get(Account, current_user.account.id)

    # Obtener el número total de followers de la cuenta
    count_statement = select(func.count()).select_from(Account).join(
        Follower, Account.id == Follower.following_id).where(Follower.follower_id == account.id)
    count = session.exec(count_statement).one()

    # Obtener los followers de la cuenta
    statement = select(Account).join(Follower, Account.id == Follower.following_id).where(
        Follower.follower_id == account.id).offset(skip).limit(limit)
    accounts_out = session.exec(statement).all()

    return AccountsOut(data=accounts_out, count=count)


@router.get("/followers/{account_id}", response_model=FollowersOut)
def read_all_followers(session: SessionDep, account_id: uuid.UUID, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all followers for the account by id
    """

    statement = select(Account).where(Account.id == account_id)
    account = session.exec(statement).first()

    if not account:
        raise HTTPException(
            status_code=404, detail="Account not found."
        )

    # Obtener el número total de followers de la cuenta
    count_statement = select(func.count()).select_from(Follower).where(Follower.following_id == account.id)
    count = session.exec(count_statement).one()

    # Obtener los followers de la cuenta
    statement = select(Follower).where(Follower.following_id == account.id).offset(skip).limit(limit)
    followers = session.exec(statement).all()

    return FollowersOut(data=followers, count=count)


@router.get("/followings/{account_id}", response_model=FollowersOut)
def read_all_following(session: SessionDep, account_id: uuid.UUID, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all followings for the accound by id
    """

    statement = select(Account).where(Account.id == account_id)
    account = session.exec(statement).first()

    if not account:
        raise HTTPException(
            status_code=404, detail="Account not found."
        )

    # Obtener el número total de follower de la cuenta
    count_statement = select(func.count()).select_from(Follower).where(Follower.follower_id == account.id)
    count = session.exec(count_statement).one()

    # Obtener las follower de la cuenta
    statement = select(Follower).where(Follower.follower_id == account.id).offset(skip).limit(limit)
    follower = session.exec(statement).all()

    return FollowersOut(data=follower, count=count)


@router.get("/followers_accounts/{account_id}", response_model=AccountsOut)
def read_all_followers_accounts(session: SessionDep, account_id: uuid.UUID, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all accounts followers for the account by id
    """

    statement = select(Account).where(Account.id == account_id)
    account = session.exec(statement).first()

    if not account:
        raise HTTPException(
            status_code=404, detail="Account not found."
        )

        # Obtener el número total de followers de la cuenta
    count_statement = select(func.count()).select_from(Account).join(
        Follower, Account.id == Follower.follower_id).where(Follower.following_id == account.id)
    count = session.exec(count_statement).one()

    # Obtener los followers de la cuenta
    statement = select(Account).join(Follower, Account.id == Follower.follower_id).where(
        Follower.following_id == account.id).offset(skip).limit(limit)
    accounts_out = session.exec(statement).all()

    return AccountsOut(data=accounts_out, count=count)


@router.get("/followings_accounts/{account_id}", response_model=FollowersOut)
def read_all_following_accounts(session: SessionDep, account_id: uuid.UUID, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all followings for the accound by id
    """

    statement = select(Account).where(Account.id == account_id)
    account = session.exec(statement).first()

    if not account:
        raise HTTPException(
            status_code=404, detail="Account not found."
        )

    # Obtener el número total de followers de la cuenta
    count_statement = select(func.count()).select_from(Account).join(
        Follower, Account.id == Follower.following_id).where(Follower.follower_id == account.id)
    count = session.exec(count_statement).one()

    # Obtener los followers de la cuenta
    statement = select(Account).join(Follower, Account.id == Follower.following_id).where(
        Follower.follower_id == account.id).offset(skip).limit(limit)
    accounts_out = session.exec(statement).all()

    return AccountsOut(data=accounts_out, count=count)


@router.get("/following_specific_account/{account_id}", response_model=AccountOut)
def read_following_specific_account(session: SessionDep, account_id: uuid.UUID, current_user: CurrentUser) -> Any:
    """
    Get followings specific accound by id
    """
    statement = select(Account).where(Account.id == account_id)
    account = session.exec(statement).first()

    statement = select(Follower).where(
        Follower.follower_id == current_user.account.id and Follower.following_id == account.id)
    follower = session.exec(statement).first()

    if not account:
        raise HTTPException(
            status_code=404, detail="Account not found."
        )
    if not follower:
        raise HTTPException(
            status_code=404, detail="Follower not found."
        )

    return account
