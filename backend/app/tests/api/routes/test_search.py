from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlmodel import Session
from app.main import app
from app import crud
from app.core.config import settings
from app.models import UserCreate
from app.tests.utils.utils import random_email, random_lower_string
import pytest
from uuid import uuid4

client = TestClient(app)

@pytest.fixture
def create_user():
    user_data = {
        "email": "editorial23@example.com",
        "password": "password123",
        "name": "new",
        "cif" :"b12345678",
        "is_editor": True
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response

@pytest.fixture
def create_account(create_user):
    user_out = create_user.json()
    user_id = user_out["id"]
    account_data = {
        "id": user_id
    }

    response = client.post("api/v1/accounts/", json=account_data)
    return response

@pytest.fixture
def create_user_2():
    user_data = {
        "email": "brandon@example.com",
        "password": "password123",
        "name": "new",
        "surname" :"user",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response
@pytest.fixture
def create_account_2(create_user_2):
    account_id = create_user_2.json()["id"]
    account_data = {
        "id": account_id
    }
    response = client.post("/api/v1/accounts/", json=account_data)
    return response

@pytest.fixture
def create_user_3():
    user_data = {
        "email": "broncano@example.com",
        "password": "password123",
        "name": "new",
        "surname" :"user",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response
@pytest.fixture
def create_account_3(create_user_3):
    account_id = create_user_3.json()["id"]
    account_data = {
        "id": account_id
    }
    response = client.post("/api/v1/accounts/", json=account_data)
    return response

@pytest.fixture
def create_user_4():
    user_data = {
        "email": "bruno@example.com",
        "password": "password123",
        "name": "new",
        "surname": "user",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response
@pytest.fixture
def create_account_4(create_user_4):
    account_id = create_user_4.json()["id"]
    account_data = {
        "id": account_id
    }
    response = client.post("/api/v1/accounts/", json=account_data)
    return response

@pytest.fixture
def create_user_5():
    user_data = {
        "email": "anabel@example.com",
        "password": "password123",
        "name": "new",
        "surname": "user",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response
@pytest.fixture
def create_account_5(create_user_5):
    account_id = create_user_5.json()["id"]
    account_data = {
        "id": account_id
    }
    response = client.post("/api/v1/accounts/", json=account_data)
    return response

@pytest.fixture
def authenticate():
    email = "editorial23@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username":email, "password":password})
    return response.json()['access_token']

@pytest.fixture
def create_book1(authenticate):
    account = client.get("/api/v1/users/by_email/editorial23@example.com")
    account_id = account.json()['id']
    book_data = {
        "title" : "El camino de los reyes",
        "author" : "Brandon Sanderson",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "9788466657662",
        "account_id" : account_id,
        "price" : 33,
        "publication_year" : 2015,
        "links": ["https://www.casadellibro.com/libro-el-camino-de-los-reyes-saga-el-archivo-de-las-tormentas-1/9788466657662/2571296"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)
    return response

@pytest.fixture
def create_book2(authenticate):
    account = client.get("/api/v1/users/by_email/editorial23@example.com")
    account_id = account.json()['id']
    book_data = {
        "title" : "Palabras Radiantes",
        "author" : "Brandon Sanderson",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "9788466657549",
        "account_id" : account_id,
        "price" : 33,
        "publication_year" : 2015,
        "links": ["https://www.casadellibro.com/libro-palabras-radiantes-saga-el-archivo-de-las-tormentas-2/9788466657549/2571295"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)
    return response

@pytest.fixture
def create_book3(authenticate):
    account = client.get("/api/v1/users/by_email/editorial23@example.com")
    account_id = account.json()['id']
    book_data = {
        "title" : "Juramentada",
        "author" : "Brandon Sanderson",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "9788417347000",
        "account_id" : account_id,
        "price" : 33,
        "publication_year" : 2015,
        "links": ["https://www.casadellibro.com/libro-juramentada-saga-el-archivo-de-las-tormentas-3/9788417347000/6311284"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)
    return response

@pytest.fixture
def create_book4(authenticate):
    account = client.get("/api/v1/users/by_email/editorial23@example.com")
    account_id = account.json()['id']
    book_data = {
        "title" : "El principe de la niebla",
        "author" : "Carlos Ruiz Zafon",
        "gender_main" : "Misterio",
        "synopsis" : "lorem ipsum",
        "isbn" : "9788408163541",
        "account_id" : account_id,
        "price" : 33,
        "publication_year" : 2015,
        "links": ["https://www.casadellibro.com/libro-el-principe-de-la-niebla/9788408163541/3104118"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)
    return response


def test_search_books_and_users(create_account, create_book1, create_book2, create_user_2):
    """
    Prueba que la query 'brandon' devuelve los libros y el usuario relacionado.
    """
    # account = create_account
    # Ejecutar el endpoint de búsqueda
    response = client.get("/api/v1/search/", params={"query": "brandon", "limit": 10})
    assert response.status_code == 200

    # Verificar el contenido de los resultados
    results = response.json()

    # Comprobar que hay exactamente 3 resultados
    assert len(results) == 3

    # Comprobar los datos de los libros
    book_titles = {result["title"] for result in results if result.get("title")}
    assert "El camino de los reyes" in book_titles
    assert "Palabras Radiantes" in book_titles

    # Comprobar los datos del usuario
    user_emails = {result["email"] for result in results if result.get("email")}
    assert "brandon@example.com" in user_emails


def test_search_with_empty_result(create_book4):
    """
    Prueba que la query que no coincide con ningún libro o usuario devuelve una lista vacía.
    """
    # Ejecutar el endpoint con una query que no debe encontrar resultados
    response = client.get("/api/v1/search/", params={"query": "nonexistentquery", "limit": 10})
    assert response.status_code == 200

    # Verificar que los resultados están vacíos
    results = response.json()
    assert len(results) == 0