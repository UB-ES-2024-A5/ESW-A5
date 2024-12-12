""" Forum reaccions models """
import uuid
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

from app.models import Account


# Relacion muchos a muchos enre forum i account: Esto es necesario porque una cuenta puede dar "like" o "dislike"
# a múltiples foros, y cada foro puede recibir "likes" o "dislikes" de múltiples cuentas.
class ForumReactionBase(SQLModel):
    type: bool  # "like" o "dislike"


class ForumReaction(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    forum_id: uuid.UUID = Field(foreign_key="forum.id")  # Relación con Forum
    forum: "Forum" = Relationship(back_populates="reactions")

    account_id: uuid.UUID = Field(foreign_key="account.id")  # Relación con Account
    account: "Account" = Relationship(back_populates="reactions")

    type: bool = Field(default=True, max_length=10)  # "like" = True o "dislike" = False


class ForumReactionUpdate(ForumReactionBase):
    pass


class ForumReactionOut(ForumReactionBase):
    id: uuid.UUID
    forum_id: uuid.UUID
    account_id: uuid.UUID
