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
        "email": "usernew2312@example.com",
        "password": "password123",
        "name": "new",
        "surname" :"user",
        "is_editor": True
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response

@pytest.fixture
def create_account(create_user):
    account_data = {
        "email": "usernew2312@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/accounts/", json=account_data)
    return response

@pytest.fixture
def create_user_2():
    user_data = {
        "email": "usernew231@example.com",
        "password": "password123",
        "name": "new",
        "surname" :"user",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response

@pytest.fixture
def create_account_2(create_user_2):
    account_data = {
        "email": "usernew231@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/accounts/", json=account_data)
    return response

def test_create_book(create_account):
    account_id = create_account.id
    book_data = {
        "title" : "Marina",
        "author" : "Carlos Ruiz Zafon",
        "genre1" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "7675453127934",
        "account_id_in" : account_id,
        "price" : 30,
        "publication_year" : 1999
    }
    response = client.post("/api/v1/books/", json=book_data)
    assert response.code == 200
    assert response.json()["title"] == book_data["title"]
    assert response.json()["isbn"] == book_data["isbn"]

def test_create_book_with_same_isbn(create_account):
    account_id = create_account.id
    book_data = {
        "title" : "Marina",
        "author" : "Carlos Ruiz Zafon",
        "genre1" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "7675453127934",
        "account_id_in" : account_id,
        "price" : 30,
        "publication_year" : 1999
    }
    response = client.post("/api/v1/books/", json=book_data)
    assert response.code == 400

def test_get_book_by_id(create_account):
    account_id = create_account.id
    book_data = {
        "title" : "Marina",
        "author" : "Carlos Ruiz Zafon",
        "genre1" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "7675453127964",
        "account_id_in" : account_id,
        "price" : 30,
        "publication_year" : 1999
    }

    response = client.post("/api/v1/books/", json=book_data)

    book_id = response.id
    response = client.get(f"api/v1/book/{book_id}")
    assert response.code == 200
    assert response.json["title"] == book_data["title"]


def test_create_book_being_normal_user(create_account_2):
    id_account = create_account_2.id
    book_data = {
        "title" : "Marina",
        "author" : "Carlos Ruiz Zafon",
        "genre1" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "9675453127964",
        "account_id_in" : id_account,
        "price" : 30,
        "publication_year" : 1999
    }

    response = client.post("/api/v1/books/", json=book_data)
    assert response.code == 400





