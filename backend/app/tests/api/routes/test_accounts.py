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
        "email": "usernew@example.com",
        "password": "password123",
        "name": "new",
        "surname" :"user",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response


def test_create_account(create_user):
    user_out = create_user.json()
    user_id = user_out["id"] 
    account_data = {
        "id": user_id
    }

    response = client.post("api/v1/accounts/", json=account_data)
    assert response.status_code == 200
    assert response.json()["id"] == user_id

def test_create_account_with_invalid_user_id():
    account_id= uuid4()
    account_data = {
        "id": account_id
    }
    response = client.post("api/v1/accounts/", json=account_data)
    assert response.status_code == 400
