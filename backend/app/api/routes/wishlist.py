""" Wishlists management routes """
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
    WishList,
    WishListCreate,
    WishListUpdate,
    WishListOut,
    WishListsOut,
    User,
    Message
)

router = APIRouter()
