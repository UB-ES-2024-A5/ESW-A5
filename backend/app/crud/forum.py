""" Forum related CRUD methods """

from typing import Any, List

from sqlmodel import Session, select
from sqlalchemy import delete
from fastapi import HTTPException

from app.core.security import get_password_hash, verify_password
from app.models import (
    User, UserCreate, UserUpdate, Forum, ForumCreate,
    ForumUpdate, ForumOut, ForumsOut, Account, ForumReaction, ForumReactionBase
)
import uuid


def create_post(session: Session, post: ForumCreate, current_user: User):
    if not post.img:
        new_post = Forum(
            text=post.text,
            account_id=current_user.id
        )
    elif not post.text:
        new_post = Forum(
            img=post.img,
            account_id=current_user.id
        )
    else:
        new_post = Forum(
            text=post.text,
            img=post.img,
            account_id=current_user.id
        )
    current_user.account.posts_forum.append(new_post)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


def create_response(session: Session, post: ForumCreate, parent_post: Forum, current_user: User):
    new_post = Forum(
        text=post.text,
        img=post.img,
        account_id=current_user.id,
        parent_forum_id=parent_post.id
    )
    current_user.account.posts_forum.append(new_post)
    parent_post.responses.append(new_post)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


def create_reaction(session: Session, db_post: Forum, reaction: ForumReactionBase, current_user: User):
    new_reaction = ForumReaction(
        forum_id=db_post.id,
        account_id=current_user.id,
        type=reaction.type
    )
    current_user.account.reactions.append(new_reaction)
    db_post.reactions.append(new_reaction)
    session.add(new_reaction)
    session.commit()
    session.refresh(new_reaction)
    return new_reaction


def update_reaction(session: Session, db_reaction: ForumReaction, new_reaction: ForumReactionBase, current_user: User):
    db_reaction.type = new_reaction.type  # Actualizem type (True = 1 , False = 0)
    session.add(db_reaction)
    session.commit()
    session.refresh(db_reaction)
    return db_reaction


def delete_post(session: Session, post: Forum):
    delete_reactions(session, post)
    session.delete(post)  # Eliminar respuesta actual
    session.commit()


def delete_responses(session: Session, post: Forum):
    for response in post.responses:
        delete_responses(session, response)  # Llamada recursiva para eliminar sub-respuestas
        delete_reactions(session, response) # Eliminar reacciones de la respuesta
        session.delete(response)  # Eliminar respuesta actual
        session.commit()


def delete_reactions(session: Session, post: Forum):
    # Eliminar todas las reacciones asociadas al post
    session.exec(delete(ForumReaction).where(ForumReaction.forum_id == post.id))
    session.commit()


def update_post(session: Session, db_post: Forum):
    likes = 0
    dislikes = 0
    for reaction in db_post.reactions:
        if reaction.type:
            likes += 1
        elif not reaction.type:
            dislikes += 1
    db_post.likes = likes
    db_post.dislikes = dislikes
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
