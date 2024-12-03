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
        "email": "usernew232@example.com",
        "password": "password123",
        "name": "Editor1",
        "cif" :"g66666666",
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
def authenticate():
    email = "usernew232@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username":email, "password":password})
    return response.json()['access_token']

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
    account_id = create_user_2.json()["id"]
    account_data = {
        "id": account_id
    }
    response = client.post("/api/v1/accounts/", json=account_data)
    return response

@pytest.fixture
def authenticate_2():
    email = "usernew231@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username":email, "password":password})
    return response.json()['access_token']

def test_create_book(create_account,authenticate):
    account_id = create_account.json()['id']
    book_data = {
        "title" : "Marina",
        "author" : "Carlos Ruiz Zafon",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "7675453127934",
        "account_id" : account_id,
        "price" : 30,
        "publication_year" : 1999,
        "links": ["https://somebooklink.com"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }
    response = client.post("/api/v1/books/", json=book_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == book_data["title"]
    assert response.json()["isbn"] == book_data["isbn"]

def test_create_book_with_same_isbn(authenticate):
    account = client.get("/api/v1/users/by_email/usernew232@example.com/")
    account_id = account.json()['id']
    book_data = {
        "title" : "Marina",
        "author" : "Carlos Ruiz Zafon",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "7675453127934",
        "account_id" : account_id,
        "price" : 30,
        "publication_year" : 1999,
        "links": ["https://somebooklink.com"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }
    response = client.post("/api/v1/books/", json=book_data,headers=headers)
    assert response.status_code == 400

def test_get_book_by_id(authenticate):
    account = client.get("/api/v1/users/by_email/usernew232@example.com/")
    account_id = account.json()['id']
    book_data = {
        "title" : "Marina",
        "author" : "Carlos Ruiz Zafon",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "7675453127964",
        "account_id" : account_id,
        "price" : 30,
        "publication_year" : 1999,
        "links": ["https://somebooklink234.com"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)

    book_id = response.json()['id']
    response = client.get(f"api/v1/books/search_id/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == book_data["title"]


def test_create_book_being_normal_user(create_account_2,authenticate_2):
    id_account = create_account_2.json()['id']
    book_data = {
        "title" : "Marina",
        "author" : "Carlos Ruiz Zafon",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "9675453127964",
        "account_id" : id_account,
        "price" : 30,
        "publication_year" : 1999,
        "links" : ["https://somebooklink2334.com"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate_2}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "User must be an editorial user."

def test_create_book_not_being_current_user():
    account = client.get("/api/v1/users/by_email/usernew232@example.com/")
    account_id = account.json()['id']
    book_data = {
        "title" : "Marina",
        "author" : "Carlos Ruiz Zafon",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "7675453127934",
        "account_id" : account_id,
        "price" : 30,
        "publication_year" : 1999,
        "links": ["https://somebooklink2.com"]
    }
    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 401
   

def test_create_book_with_repeated_links(authenticate):
    account = client.get("/api/v1/users/by_email/usernew232@example.com/")
    account_id = account.json()['id']
    book_data = {
        "title" : "Marina",
        "author" : "Carlos Ruiz Zafon",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "1675453127964",
        "account_id" : account_id,
        "price" : 30,
        "publication_year" : 1999,
        "links": ["https://somebooklink.com"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)
    assert response.status_code == 400


def test_create_book_with_isbn_with_less_than_10_digits(authenticate):
    account = client.get("/api/v1/users/by_email/usernew232@example.com/")
    account_id = account.json()['id']
    book_data = {
        "title" : "Marina",
        "author" : "Carlos Ruiz Zafon",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "64",
        "account_id" : account_id,
        "price" : 30,
        "publication_year" : 1999,
        "links": ["https://somebookinglink.com"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)
    assert response.status_code == 422


def test_create_book_with_isbn_with_more_than_13_digits(authenticate):
    account = client.get("/api/v1/users/by_email/usernew232@example.com/")
    account_id = account.json()['id']
    book_data = {
        "title" : "Marina",
        "author" : "Carlos Ruiz Zafon",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "64282828282828",
        "account_id" : account_id,
        "price" : 30,
        "publication_year" : 1999,
        "links": ["https://somebookinglink.com"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)
    assert response.status_code == 422

def test_get_all_my_books_not_editor(authenticate_2):
    account = client.get("/api/v1/users/by_email/usernew231@example.com/")

    headers = {
        "Authorization": f"Bearer {authenticate_2}"
    }

    response = client.get("/api/v1/books/my_books", headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "User must be an editorial user."

def test_get_all_my_books(authenticate):
    account = client.get("/api/v1/users/by_email/usernew232@example.com/")
    account_id = account.json()['id']

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.get("/api/v1/books/my_books", headers=headers)
    assert response.status_code == 200

    results = response.json()
    print(results)
    assert len(results) == 2 # Hay dos marinas repetidos con diferente isbn

    book_titles = {book["title"] for book in results["data"] if book.get("title")}
    assert "Marina" in book_titles