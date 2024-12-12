""" Forums management routes """

import uuid

from typing import Any, Optional

from sqlmodel import col, delete, func, select
from fastapi import APIRouter, Depends, HTTPException

from app import crud
from app.api.deps import (
    CurrentUser, SessionDep, get_current_active_superuser,
)

from app.models import (
    Forum, ForumCreate, ForumOut, ForumsOut, User, Message, Account, Link, LinkOut, LinksOut,
    LinkUpdate, Follower, ForumReactionBase, ForumReaction, ForumReactionOut
)

router = APIRouter()


@router.get("/all_posts_me/", response_model=ForumsOut)
def read_all_me_posts(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all me posts in forum (both posts and responses).
    """
    count_statement = select(func.count()).select_from(Forum).where(Forum.account_id == current_user.id)
    count = session.exec(count_statement).one()

    statement = select(Forum).where(Forum.account_id == current_user.id).offset(skip).limit(limit)
    forums = session.exec(statement).all()

    return ForumsOut(data=forums, count=count)


@router.get("/all_posts/{account_id}", response_model=ForumsOut)
def read_all_posts_and_responses_by_account_id(session: SessionDep, account_id: uuid.UUID, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all posts by account_id in forum (both posts and responses).
    """
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(
            status_code=404, detail="Account does not exist"
        )

    count_statement = select(func.count()).select_from(Forum).where(Forum.account_id == account_id)
    count = session.exec(count_statement).one()

    statement = select(Forum).where(Forum.account_id == account_id).offset(skip).limit(limit)
    forums = session.exec(statement).all()

    return ForumsOut(data=forums, count=count)


@router.get("/post_by_id/{post_id}", response_model=ForumOut)
def read_post_by_id(session: SessionDep, post_id: uuid.UUID, skip: int = 0, limit: int = 100) -> Any:
    """
    Get post by id
    """
    statement = select(Forum).where(Forum.id == post_id)
    post = session.exec(statement).first()
    if not post:
        raise HTTPException(
            status_code=404, detail="Post does not exist"
        )

    return post


@router.get("/all_post_my_following/", response_model=ForumsOut)
def read_all_posts_my_followings(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all posts from my followings (Posts only, no responses)
    """
    statement = select(Account).join(Follower, Account.id == Follower.following_id).where(
        Follower.follower_id == current_user.id).offset(skip).limit(limit)
    accounts_followings = session.exec(statement).all()

    count = 0
    forums = []

    for account_follow in accounts_followings:
        count_statement = select(func.count()).select_from(Forum).where(
            Forum.account_id == account_follow.id,
            Forum.parent_forum_id == None)
        count += session.exec(count_statement).one()

        statement = select(Forum).where(
            Forum.account_id == account_follow.id,
            Forum.parent_forum_id == None
        ).offset(skip).limit(limit)
        forums.extend(session.exec(statement).all())

    return ForumsOut(data=forums, count=count)


@router.get("/responses/{post_id}", response_model=ForumsOut)
def read_all_responses_by_post(session: SessionDep, post_id: uuid.UUID, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all post responses by post id
    """
    statement = select(Forum).where(Forum.id == post_id)
    post = session.exec(statement).first()
    if not post:
        raise HTTPException(
            status_code=404, detail="Post does not exist"
        )

    count_statement = select(func.count()).select_from(Forum).where(Forum.parent_forum_id == post_id)
    count = session.exec(count_statement).one()

    statement = select(Forum).where(Forum.parent_forum_id == post_id).offset(skip).limit(limit)
    forums_responses = session.exec(statement).all()

    return ForumsOut(data=forums_responses, count=count)


@router.post("/", response_model=ForumOut)
async def create_post(*, session: SessionDep, current_user: CurrentUser, post: ForumCreate):
    """
    Create new post/response in forum.
    """
    db_obj = crud.forum.create_post(session=session, post=post, current_user=current_user)

    return db_obj


@router.post("/{post_parent_id}", response_model=ForumOut)
async def create_response(*, session: SessionDep, current_user: CurrentUser, post: ForumCreate, post_parent_id: uuid.UUID):
    statement = select(Forum).where(Forum.id == post_parent_id)
    parent_post = session.exec(statement).first()

    if not parent_post:
        raise HTTPException(
            status_code=404, detail="Parent post does not exist"
        )

    db_obj = crud.forum.create_response(session=session, post=post, parent_post=parent_post, current_user=current_user)

    return db_obj


@router.delete("/delete_post/{post_id}")
def delete_post(session: SessionDep, current_user: CurrentUser, post_id: uuid.UUID) -> Message:
    """
    Delete a post in the forum along with all its responses and reactions.
    """
    statement = select(Forum).where(Forum.id == post_id)
    post = session.exec(statement).first()
    if not post:
        raise HTTPException(
            status_code=404, detail="Post does not exist"
        )

    statement = select(Forum).where(Forum.id == post_id)
    db_post = session.exec(statement).first()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post forum not found")

    elif not (current_user.account.id == db_post.account.id):
        raise HTTPException(
            status_code=403, detail="This post forum does not belong to your user"
        )

    crud.forum.delete_responses(session=session, post=db_post)
    crud.forum.delete_post(session=session, post=db_post)

    return Message(message="Post Forum deleted successfully")


@router.post("/create_reaction/{post_id}", response_model=ForumReactionOut)
async def create_reaction_post(*, session: SessionDep, current_user: CurrentUser, reaction: ForumReactionBase, post_id: uuid.UUID):
    """
    Create reaction post forum.
    """

    statement = select(Forum).where(Forum.id == post_id)
    db_post = session.exec(statement).first()
    if not db_post:
        raise HTTPException(
            status_code=404, detail="Post Forum does not exist"
        )

    statement = select(ForumReaction).where(
        ForumReaction.account_id == current_user.id,
        ForumReaction.forum_id == post_id
    )
    db_reaction = session.exec(statement).first()
    if db_reaction:
        raise HTTPException(
            status_code=400, detail="Reaction already exists."
        )

    new_reaction = crud.forum.create_reaction(session=session, db_post=db_post, reaction=reaction, current_user=current_user)
    crud.forum.update_post(session=session, db_post=db_post)

    return new_reaction


@router.patch("/update_reaction/{post_id}", response_model=ForumReactionOut)
def update_reaction(*, session: SessionDep, current_user: CurrentUser, new_reaction: ForumReactionBase, post_id: uuid.UUID):
    """
    Update reaction post forum.
    """
    statement = select(Forum).where(Forum.id == post_id)
    post = session.exec(statement).first()
    if not post:
        raise HTTPException(
            status_code=404, detail="Post does not exist"
        )

    statement = select(Forum).where(Forum.id == post_id)
    db_post = session.exec(statement).first()
    if not db_post:
        raise HTTPException(
            status_code=404, detail="Post Forum does not exist"
        )

    statement = select(ForumReaction).where(
        ForumReaction.account_id == current_user.id,
        ForumReaction.forum_id == post_id
    )
    db_reaction = session.exec(statement).first()
    if not db_reaction:
        raise HTTPException(
            status_code=400, detail="Reaction does not exists."
        )

    up_reaction = crud.forum.update_reaction(session=session, db_reaction=db_reaction, new_reaction=new_reaction, current_user=current_user)
    crud.forum.update_post(session=session, db_post=db_post)

    return up_reaction


@router.delete("/delete_reaction/{post_id}")
def delete_reaction(*, session: SessionDep, current_user: CurrentUser, post_id: uuid.UUID) -> Message:
    """
    Delete reaction post forum.
    """
    statement = select(Forum).where(Forum.id == post_id)
    post = session.exec(statement).first()
    if not post:
        raise HTTPException(
            status_code=404, detail="Post does not exist"
        )

    statement = select(Forum).where(Forum.id == post_id)
    db_post = session.exec(statement).first()
    if not db_post:
        raise HTTPException(
            status_code=404, detail="Post Forum does not exist"
        )
    if not db_post.account_id == current_user.id:
        raise HTTPException(
            status_code=403, detail="This post does not belong to your account"
        )

    statement = select(ForumReaction).where(
        ForumReaction.account_id == current_user.id,
        ForumReaction.forum_id == post_id
    )
    db_reaction = session.exec(statement).first()

    if not db_reaction:
        raise HTTPException(
            status_code=400, detail="Reaction does not exists."
        )

    session.delete(db_reaction)
    session.commit()
    crud.forum.update_post(session=session, db_post=db_post)

    return Message(message="Reaction successfully removed")

@router.get("/posts_me_like/", response_model=ForumsOut)
def read_me_posts_like(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all posts I've liked on the forum
    """

    count_statement = select(func.count()).select_from(ForumReaction).where(
        ForumReaction.account_id == current_user.id,
        ForumReaction.type == True
    )
    count = session.exec(count_statement).one()

    statement = select(Forum).join(
        ForumReaction, Forum.id == ForumReaction.forum_id).where(
        ForumReaction.account_id == current_user.id,
        ForumReaction.type == True
    ).offset(skip).limit(limit)
    forums_out = session.exec(statement).all()

    return ForumsOut(data=forums_out, count=count)


@router.get("/posts_me_dislike/", response_model=ForumsOut)
def read_me_posts_dislike(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all posts I've disliked on the forum by account id
    """

    count_statement = select(func.count()).select_from(ForumReaction).where(
        ForumReaction.account_id == current_user.id,
        ForumReaction.type == False
    )
    count = session.exec(count_statement).one()

    statement = select(Forum).join(
        ForumReaction, Forum.id == ForumReaction.forum_id).where(
        ForumReaction.account_id == current_user.id,
        ForumReaction.type == False
    ).offset(skip).limit(limit)
    forums_out = session.exec(statement).all()

    return ForumsOut(data=forums_out, count=count)


@router.get("/posts_like/{account_id}", response_model=ForumsOut)
def read_posts_like(session: SessionDep, account_id: uuid.UUID, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all posts I've liked on the forum by account id
    """
    statement = select(Account).where(Account.id == account_id)
    account = session.exec(statement).first()
    if not account:
        raise HTTPException(
            status_code=404, detail="Account does not exist"
        )
    count_statement = select(func.count()).select_from(ForumReaction).where(
        ForumReaction.account_id == account_id,
        ForumReaction.type == True
    )
    count = session.exec(count_statement).one()

    statement = select(Forum).join(
        ForumReaction, Forum.id == ForumReaction.forum_id).where(
        ForumReaction.account_id == account_id,
        ForumReaction.type == True
    ).offset(skip).limit(limit)
    forums_out = session.exec(statement).all()

    return ForumsOut(data=forums_out, count=count)


@router.get("/posts_dislike/{account_id}", response_model=ForumsOut)
def read_posts_dislike(session: SessionDep, account_id: uuid.UUID, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all posts I've disliked on the forum
    """
    statement = select(Account).where(Account.id == account_id)
    account = session.exec(statement).first()
    if not account:
        raise HTTPException(
            status_code=404, detail="Account does not exist"
        )

    count_statement = select(func.count()).select_from(ForumReaction).where(
        ForumReaction.account_id == account_id,
        ForumReaction.type == False
    )
    count = session.exec(count_statement).one()

    statement = select(Forum).join(
        ForumReaction, Forum.id == ForumReaction.forum_id).where(
        ForumReaction.account_id == account_id,
        ForumReaction.type == False
    ).offset(skip).limit(limit)
    forums_out = session.exec(statement).all()

    return ForumsOut(data=forums_out, count=count)
