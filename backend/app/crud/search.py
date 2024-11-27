""" Searches related CRUD methods """
from sqlmodel import Session, select
from sqlalchemy import or_
from sqlalchemy.sql.operators import ilike_op
from typing import List, Union, Any
from app.models import Book, User  # Asegúrate de importar los modelos correctos
from app.crud.book import convert_book_bookOut

def query_items(session: Session, query: str, limit: int) -> Any:
    # Búsqueda en libros
    book_statement = (
        select(Book)
        .where(
            or_(
                ilike_op(Book.title, f"%{query}%"),
                ilike_op(Book.author, f"%{query}%"),
                ilike_op(Book.isbn, f"%{query}%"),
            )
        )
    )
    book_results = session.exec(book_statement).all()

    # Búsqueda en usuarios
    user_statement = (
        select(User)
        .where(ilike_op(User.email, f"%{query}%"),)
    )
    user_results = session.exec(user_statement).all()

    # Combinar resultados en una sola lista
    combined_results = []

    for book in book_results:
        converted_book = convert_book_bookOut(book)
        combined_results.append({"type": "book", "data": converted_book, "score": 1})

    for user in user_results:
        combined_results.append({"type": "user", "data": user, "score": 1})

    # Ordenar por puntuación y limitar a los limit más relevantes
    combined_results.sort(key=lambda x: x["score"], reverse=True)

    return combined_results[:limit]