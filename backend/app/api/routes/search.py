""" Searches management routes """
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Any
from sqlmodel import col, delete, func, select

from app import crud

from app.api.deps import (
    SessionDep
)

from app.models import (
    UserPublic,
    BookOut
)


router = APIRouter()

@router.get("/")
def get_search(*, session: SessionDep, query: str, limit: int = 10) -> Any:
    """
    Gets a list of books and users matching the query.
    """
    results = crud.search.query_items(query=query, limit=limit, session=session)

    # Convertir los resultados para la respuesta
    response = []
    for result in results:
        if result["type"] == "book":
            response.append(BookOut.from_orm(result["data"]))
        elif result["type"] == "user":
            response.append(UserPublic.from_orm(result["data"]))

    return response