""" Comment models """
import uuid

from sqlmodel import Field, Relationship
from .base import SQLModel

class CommentBase(SQLModel):
    text: str = Field(max_length=255)

class Comment(CommentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    review_id: uuid.UUID = Field(foreign_key="review.id")
    review: "Review" = Relationship(back_populates="comments")

class CommentOut(CommentBase):
    id: uuid.UUID

class CommentsOut(SQLModel):
    data: list[CommentOut]
    count: int

class CommentUpdate(SQLModel):
    text: str

