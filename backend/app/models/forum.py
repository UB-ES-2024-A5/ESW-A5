""" Forum models """

import uuid
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


# Base para el post
class ForumBase(SQLModel):
    text: str | None = Field(default=None, max_length=255)  # Texto opcional
    img: str | None = Field(default=None)  # URL de la imagen opcional


def current_time():
    return datetime.now(timezone.utc)
# Tabla principal del post
class Forum(ForumBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    account_id: uuid.UUID = Field(foreign_key="account.id")  # Relación con Account
    account: "Account" = Relationship(back_populates="posts_forum")

    parent_forum_id: uuid.UUID | None = Field(foreign_key="forum.id")  # Respuesta a otro post
    parent_forum: Optional["Forum"] = Relationship(back_populates="responses")
    responses: List["Forum"] = Relationship(back_populates="parent_forum")

    date: datetime = Field(default_factory=current_time)
    likes: int = Field(default=0)  # Contador de likes
    dislikes: int = Field(default=0)  # Contador de dislikes

    # Relación con las reacciones de los usuarios (likes y dislikes)
    reactions: List["ForumReaction"] = Relationship(back_populates="forum")


# Modelos para las operaciones CRUD
# Crear un post
class ForumCreate(ForumBase):
    author_id: uuid.UUID  # ID del autor
    parent_post_id: uuid.UUID | None = None  # ID del post padre (opcional)


# Actualizar likes y dislikes
class ForumReaction(SQLModel):
    type: bool  # "like" o "dislike"


class ForumUpdate(ForumBase):
    pass

# Modelo de salida de un post
class ForumOut(ForumBase):
    id: uuid.UUID
    account_id: uuid.UUID
    parent_forum_id: uuid.UUID | None
    date: datetime
    likes: int
    dislikes: int


# Modelo de salida con lista de posts
class ForumsOut(SQLModel):
    data: List[ForumOut]
    count: int
