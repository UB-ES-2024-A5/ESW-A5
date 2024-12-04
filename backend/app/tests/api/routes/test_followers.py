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
        "email": "userexample1@example.com",
        "password": "password123",
        "name": "user",
        "surname": "example1",
        "is_editor": False
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
    email = "userexample1@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username":email, "password":password})
    return response.json()['access_token']

@pytest.fixture
def create_user_2():
    user_data = {
        "email": "userexample2@example.com",
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
    email = "userexample2@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username":email, "password":password})
    return response.json()['access_token']

def test_add_followed(create_account, create_account_2, authenticate):
    account1_id = create_account.json()['id']
    account2_id = create_account_2.json()['id']

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post(f"/api/v1/followers/{account2_id}", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert result["follower_id"] == account1_id
    assert result["following_id"] == account2_id

def test_add_followed_not_found(authenticate):
    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    random_id = uuid4()

    response = client.post(f"/api/v1/followers/{random_id}", headers=headers)
    assert response.status_code == 404
    result = response.json()
    assert result["detail"] == "Account not found."

def test_add_followed_self(authenticate):
    account = client.get("/api/v1/users/by_email/userexample1@example.com")
    account_id = account.json()['id']

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post(f"/api/v1/followers/{account_id}", headers=headers)
    assert response.status_code == 403
    result = response.json()
    assert result["detail"] == "You can't follow yourself."

def test_add_followed_duplicate(authenticate):
    account1 = client.get("/api/v1/users/by_email/userexample1@example.com")
    account_id1 = account1.json()['id']

    account2 = client.get("/api/v1/users/by_email/userexample2@example.com")
    account_id2 = account2.json()['id']

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post(f"/api/v1/followers/{account_id2}", headers=headers)
    assert response.status_code == 404
    result = response.json()
    assert result["detail"] == "Follower exist."

def test_unfollow(authenticate):
    account2 = client.get("/api/v1/users/by_email/userexample2@example.com")
    account_id2 = account2.json()['id']

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.delete(f"/api/v1/followers/{account_id2}", headers=headers)
    assert response.status_code == 200

    result = response.json()
    assert result["message"] == "Unfollow successfully"

def test_unfollow_not_found(authenticate):
    random_id = uuid4()

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.delete(f"/api/v1/followers/{random_id}", headers=headers)
    assert response.status_code == 404

    result = response.json()
    assert result["detail"] == "Account not found."

def test_unfollow_not_exist(authenticate_2):
    account = client.get("/api/v1/users/by_email/userexample1@example.com")
    account_id = account.json()['id']

    headers = {
        "Authorization": f"Bearer {authenticate_2}"
    }

    response = client.delete(f"/api/v1/followers/{account_id}", headers=headers)
    assert response.status_code == 404

    result = response.json()
    assert result["detail"] == "Follower not found."
