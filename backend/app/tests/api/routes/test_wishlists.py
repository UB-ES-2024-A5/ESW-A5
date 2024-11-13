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
        "email": "editorial99@example.com",
        "password": "password123",
        "name": "new",
        "cif" :"b32546798",
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
def create_super_user():
    user_data = {
        "email": "superuser@example.com",
        "password": "password123",
        "name": "new",
        "surname" :"super",
        "is_editor": False,
        "is_superuser" : True
    
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response

@pytest.fixture
def create_account_super(create_super_user):
    user_out = create_super_user.json()
    user_id = user_out["id"] 
    account_data = {
        "id": user_id
    }

    response = client.post("api/v1/accounts/", json=account_data)
    return response

@pytest.fixture
def authenticate_2():
    email = "superuser@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username":email, "password":password})
    return response.json()['access_token']



@pytest.fixture
def authenticate():
    email = "editorial99@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username":email, "password":password})
    return response.json()['access_token']

@pytest.fixture
def create_book(authenticate):
    account = client.get("/api/v1/users/user/editorial99@example.com")
    account_id = account.json()['id']
    book_data = {
        "title" : "Marina",
        "author" : "Carlos Ruiz Zafon",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "5575453127934",
        "account_id" : account_id,
        "price" : 30,
        "publication_year" : 1999,
        "links": ["https://linkexample.com"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)
    return response

def test_create_wishlist(create_account,authenticate):
    account = create_account
    wishlist_data = {
        "name" : "Wishlist 1",
        "description" : "Compras navideñas"
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }
    
    response = client.post("/api/v1/wishlists/", json=wishlist_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["description"] == wishlist_data["description"]

def test_get_all_wishlists_all():
    response = client.get("/api/v1/wishlists/")
    assert response.status_code == 200
    print(response.json())
    assert response.json()["data"][0]["name"] == "Wishlist 1"
    assert response.json()["count"] == 1

def test_get_my_wishlists(authenticate):
    headers = {
        "Authorization": f"Bearer {authenticate}"
    }
    response = client.get("/api/v1/wishlists/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["count"] == 1

def test_get_wishlist_by_id(create_account_super, authenticate_2):
    account = create_account_super
    response = client.get("/api/v1/wishlists/")
    id_wishlist = response.json()["data"][0]["id"]

    headers = {
        "Authorization": f"Bearer {authenticate_2}"
    }

    response = client.get(f"/api/v1/wishlists/{id_wishlist}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Wishlist 1"

def test_add_book_to_wishlist(create_book,authenticate):
    headers = {
        "Authorization": f"Bearer {authenticate}"
    }
    response = client.get("/api/v1/wishlists/me", headers=headers)
    wishlist_id = response.json()["data"][0]['id']
    book_id = create_book.json()['id']

    response = client.patch(f"/api/v1/wishlists/{wishlist_id}/{book_id}", headers=headers)
    assert response.status_code == 200
    print(response.json())
    assert response.json()["message"] == "Book added correctly"

def test_add_book_to_non_own_wishlist(authenticate, authenticate_2):
    headers1 = {
        "Authorization": f"Bearer {authenticate}"
    }
    headers2 = {
        "Authorization": f"Bearer {authenticate_2}"
    }

    response = client.get("/api/v1/wishlists/me", headers=headers1)
    wishlist_id = response.json()["data"][0]['id']
    books = client.get("/api/v1/books/my_books", headers=headers1)
    book_id = books.json()["data"][0]['id']
    response = client.patch(f"/api/v1/wishlists/{wishlist_id}/{book_id}", headers=headers2)
    assert response.status_code == 422


def test_add_repeated_book_to_wishlist(authenticate):
    headers = {
        "Authorization": f"Bearer {authenticate}"
    }
    books = client.get("/api/v1/books/my_books", headers=headers)
    response = client.get("/api/v1/wishlists/me", headers=headers)
    wishlist_id = response.json()["data"][0]['id']
    book_id = books.json()['data'][0]['id']
    update = client.patch(f"/api/v1/wishlists/{wishlist_id}/{book_id}", headers=headers)
    assert update.status_code == 400

def test_add_book_to_not_existent_wishlist(authenticate):
    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    books = client.get("/api/v1/books/my_books", headers=headers)
    wishlist_id = uuid4()

    book_id = books.json()['data'][0]['id']
    update = client.patch(f"/api/v1/wishlists/{wishlist_id}/{book_id}", headers=headers)
    assert update.status_code == 404

def test_add_not_existent_book_to_wishlist(authenticate):
    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    book_id = uuid4()
    response = client.get("/api/v1/wishlists/me", headers=headers)
    wishlist_id = response.json()["data"][0]['id']

    update = client.patch(f"/api/v1/wishlists/{wishlist_id}/{book_id}",headers=headers)
    assert update.status_code == 404


def test_read_books_from_wishlist(authenticate):
    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.get("/api/v1/wishlists/me", headers=headers)
    wishlist_id = response.json()["data"][0]['id']

    response = client.get(f"/api/v1/wishlists/{wishlist_id}/books")
    assert response.status_code == 200
    assert response.json()['data'][0]['title'] == "Marina"

def test_delete_not_my_book_from_wishlist(authenticate,authenticate_2):
    headers1 = {
        "Authorization": f"Bearer {authenticate}"
    }
    headers2 = {
        "Authorization": f"Bearer {authenticate_2}"
    }
    response = client.get("/api/v1/wishlists/me", headers=headers1)
    wishlist_id = response.json()["data"][0]['id']
    books = client.get("/api/v1/books/my_books", headers=headers1)
    book_id = books.json()["data"][0]['id']
    response = client.delete(f"/api/v1/wishlists/{wishlist_id}/{book_id}", headers=headers2)
    assert response.status_code == 422

def test_delete_book_from_wishlist(authenticate):
    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.get("/api/v1/wishlists/me", headers=headers)
    wishlist_id = response.json()["data"][0]['id']
    books = client.get("/api/v1/books/my_books", headers=headers)
    book_id = books.json()["data"][0]['id']

    response = client.delete(f"/api/v1/wishlists/{wishlist_id}/{book_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Book removed from wishlist successfully"

def test_delete_not_my_wishlist(authenticate,authenticate_2):
    headers1 = {
        "Authorization": f"Bearer {authenticate}"
    }
    headers2 = {
        "Authorization": f"Bearer {authenticate_2}"
    }

    response = client.get("/api/v1/wishlists/me", headers=headers1)
    wishlist_id = response.json()["data"][0]['id']

    response = client.delete(f"/api/v1/wishlists/{wishlist_id}", headers=headers2)
    assert response.status_code == 422

def test_delete_wishlist(authenticate):
    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.get("/api/v1/wishlists/me", headers=headers)
    wishlist_id = response.json()["data"][0]['id']

    response = client.delete(f"/api/v1/wishlists/{wishlist_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Wishlist deleted successfully"


def test_delete__not_existing_wishlist(authenticate):
    headers = {
        "Authorization": f"Bearer {authenticate}"
    }


    wishlist_id = uuid4()

    response = client.delete(f"/api/v1/wishlists/{wishlist_id}", headers=headers)

    assert response.status_code == 404



