""" Searches related CRUD methods """
from sqlmodel import Session, select
from typing import List, Union
from app.models import Book, User  # Asegúrate de importar los modelos correctos

def query_items(session: Session, query: str, limit: int) -> List[Union[Book, User]]:
    # Búsqueda en libros
    book_statement = (
        select(Book)
        .where(
            (Book.title.ilike(f"%{query}%"))
            | (Book.author.ilike(f"%{query}%"))
            | (Book.isbn.ilike(f"%{query}%"))
        )
    )
    book_results = session.exec(book_statement).all()

    # Búsqueda en usuarios
    user_statement = (
        select(User)
        .where(User.email.ilike(f"%{query}%"))
    )
    user_results = session.exec(user_statement).all()

    # Combinar resultados en una sola lista
    combined_results = []

    for book in book_results:
        combined_results.append({"type": "book", "data": book, "score": 1})

    for user in user_results:
        combined_results.append({"type": "user", "data": user, "score": 1})

    # Ordenar por puntuación y limitar a los n más relevantes
    combined_results.sort(key=lambda x: x["score"], reverse=True)

    return combined_results[:limit]