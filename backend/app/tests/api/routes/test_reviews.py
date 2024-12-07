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
        "email": "userreview1@example.com",
        "password": "password123",
        "name": "nuevo",
        "surname": "palo",
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
    email = "userreview1@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username": email, "password": password})
    return response.json()['access_token']

@pytest.fixture
def create_user2():
    user_data = {
        "email": "userreview2@example.com",
        "password": "password123",
        "name": "nuevo",
        "surname": "palo2",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response

@pytest.fixture
def create_account2(create_user2):
    user_out = create_user2.json()
    user_id = user_out['id']
    account_data = {
        "id": user_id
    }

    response = client.post("/api/v1/accounts/", json=account_data)
    return response
@pytest.fixture
def authenticate2():
    email = "userreview2@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username": email, "password": password})
    return response.json()['access_token']

# Variable para almacenar datos entre pruebas
created_account_data = {}

