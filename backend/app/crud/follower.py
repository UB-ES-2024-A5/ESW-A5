""" Follower related CRUD methods """

from typing import Any, List

from sqlmodel import Session, select
from fastapi import HTTPException

from app.core.security import get_password_hash, verify_password
from app.models import (
    User, UserCreate, UserUpdate, Follower, FollowerCreate,
    FollowerUpdate, FollowerOut, FollowersOut, Account
)
import uuid


def create_follow(session: Session, account: Account, current_user: User):
    new_follower = Follower(
        follower_id=current_user.account.id,
        following_id=account.id
    )
    session.add(new_follower)
    update_num_follows(session=session, account_following=account, account_current_user=current_user.account, follow=True)

    session.commit()
    session.refresh(new_follower)
    return new_follower

def update_num_follows(session: Session, account_following: Account, account_current_user: Account, follow: bool):
    if follow:
        if account_following.num_followers is None:
            account_following.num_followers = 0
        account_following.num_followers += 1

        if account_current_user.num_following is None:
            account_current_user.num_following = 0
        account_current_user.num_following += 1
    else:
        account_following.num_followers -= 1
        account_current_user.num_following -= 1

        if account_following.num_followers < 0:
            account_following.num_followers = 0
        if account_current_user.num_following < 0:
            account_current_user.num_following = 0

    session.commit()
    session.refresh(account_following)
    session.refresh(account_current_user)


def delete_follow(session: Session, account: Account, current_user: User, follow: Follower):
    session.delete(follow)
    update_num_follows(session=session, account_following=account, account_current_user=current_user.account, follow=False)
    session.commit()



