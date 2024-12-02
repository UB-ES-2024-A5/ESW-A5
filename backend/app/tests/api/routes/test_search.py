from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlmodel import Session
from app.main import app
from app import crud
from app.core.config import settings

from uuid import uuid4
import pytest
from app.tests.utils.utils import random_email, random_lower_string

client = TestClient(app)

@pytest.fixture
def create_user():
    user_data = {
        "email": "editor23@example.com",
        "password": "password123",
        "name": "Editor1",
        "cif": "g66666666",
        "is_editor": True
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response

@pytest.fixture
def create_account(create_user):
    user_out = create_user.json()
    user_id = user_out['id']
    account_data = {
        "id": user_id
    }

    response = client.post("/api/v1/accounts/", json=account_data)
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
    email = "editor23@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username":email, "password":password})
    return response.json()['access_token']

@pytest.fixture
def create_book1(authenticate):
    account = client.get("/api/v1/users/by_email/editor23@example.com")
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
    account = client.get("/api/v1/users/by_email/editor23@example.com")
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
    account = client.get("/api/v1/users/by_email/editor23@example.com")
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
    account = client.get("/api/v1/users/by_email/editor23@example.com")
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
