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


def test_search_books_and_users(create_account, create_book1, create_book2, create_book3, create_book4, create_account_2, create_account_3, create_account_4, create_account_5):
    """
    Prueba que la query 'brandon' devuelve los libros y el usuario relacionado.
    """

    response = client.get("/api/v1/search/brandon", params={"limit": 10})
    assert response.status_code == 200

    results = response.json()
    assert len(results) == 10

    book_titles = {result["title"] for result in results if result.get("title")}
    assert "El camino de los reyes" in book_titles
    assert "Palabras Radiantes" in book_titles
    assert "Juramentada" in book_titles

    user_emails = {result["email"] for result in results if result.get("email")}
    assert "brandon@example.com" in user_emails

def test_search_books_and_users2():
    """
    Prueba que la query 'br' devuelve los libros y el usuario relacionado.
    """

    response = client.get("/api/v1/search/br", params={"limit": 10})
    assert response.status_code == 200

    results = response.json()
    assert len(results) == 12

    book_titles = {result["title"] for result in results if result.get("title")}
    assert "El camino de los reyes" in book_titles
    assert "Palabras Radiantes" in book_titles
    assert "Juramentada" in book_titles

    user_emails = {result["email"] for result in results if result.get("email")}
    assert "brandon@example.com" in user_emails
    assert "bruno@example.com" in user_emails
    assert "broncano@example.com" in user_emails

def test_search_books_by_isbn():
    """
    Prueba que la query '9788408163541' devuelve el libro relacionado
    """

    response = client.get("/api/v1/search/9788408163541", params={"limit": 10})
    assert response.status_code == 200

    results = response.json()
    assert len(results) == 1

    book_titles = {result["title"] for result in results if result.get("title")}
    assert "El principe de la niebla" in book_titles

def test_search_books_by_title():
    """
    Prueba que la query 'El' devuelve el libro relacionado
    """

    response = client.get("/api/v1/search/El", params={"limit": 10})
    assert response.status_code == 200

    results = response.json()
    assert len(results) == 7

    book_titles = {result["title"] for result in results if result.get("title")}
    assert "El principe de la niebla" in book_titles
    assert "El camino de los reyes" in book_titles

    user_emails = {result["email"] for result in results if result.get("email")}
    assert "anabel@example.com" in user_emails

def test_search_books_by_title2():
    """
    Prueba que la query 'El camino' devuelve el libro relacionado
    """

    response = client.get("/api/v1/search/El camino", params={"limit": 10})
    assert response.status_code == 200

    results = response.json()
    assert len(results) == 1

    book_titles = {result["title"] for result in results if result.get("title")}
    assert "El camino de los reyes" in book_titles


def test_search_with_empty_result():
    """
    Prueba que la query que no coincide con ningún libro o usuario devuelve una lista vacía.
    """
    response = client.get("/api/v1/search/nonexistentquery", params={"limit": 10})
    assert response.status_code == 200

    results = response.json()
    assert len(results) == 0