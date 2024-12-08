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

@pytest.fixture(scope="session")
def create_super_user():
    user_data = {
        "email": "superuser2@example.com",
        "password": "password123",
        "name": "new",
        "surname" :"super",
        "is_editor": False,
        "is_superuser" : True

    }
    response = client.post("/api/v1/users/", json=user_data)
    return response

@pytest.fixture(scope="session")
def create_account_super(create_super_user):
    user_out = create_super_user.json()
    user_id = user_out["id"]
    account_data = {
        "id": user_id
    }

    response = client.post("api/v1/accounts/", json=account_data)
    if response.status_code == 200:
        return response  # Devuelve la respuesta original si la creación es exitosa
    elif response.status_code == 400 and "Account already exists" in response.json().get("detail", ""):
        # Si ya existe, recuperar la cuenta para reutilizarla
        return client.get(f"/api/v1/accounts/{user_id}")
    else:
        raise Exception(f"Failed to create or retrieve account: {response.json()}")

@pytest.fixture
def authenticate_super():
    email = "superuser2@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username":email, "password":password})
    return response.json()['access_token']

@pytest.fixture(scope="session")
def create_user2():
    user_data = {
        "email": "usernew2@example.com",
        "password": "password123",
        "name": "new",
        "surname" :"user",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response

@pytest.fixture(scope="session")
def create_account2(create_user2):
    user_out = create_user2.json()
    user_id = user_out["id"]
    account_data = {
        "id": user_id
    }

    response = client.post("api/v1/accounts/", json=account_data)
    if response.status_code == 200:
        return response  # Devuelve la respuesta original si la creación es exitosa
    elif response.status_code == 400 and "Account already exists" in response.json().get("detail", ""):
        # Si ya existe, recuperar la cuenta para reutilizarla
        return client.get(f"/api/v1/accounts/{user_id}")
    else:
        raise Exception(f"Failed to create or retrieve account: {response.json()}")

@pytest.fixture(scope="session")
def create_user3():
    user_data = {
        "email": "usernew3@example.com",
        "password": "password123",
        "name": "new",
        "surname" :"user",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response

@pytest.fixture(scope="session")
def create_account3(create_user3):
    user_out = create_user3.json()
    user_id = user_out["id"]
    account_data = {
        "id": user_id
    }

    response = client.post("api/v1/accounts/", json=account_data)
    if response.status_code == 200:
        return response  # Devuelve la respuesta original si la creación es exitosa
    elif response.status_code == 400 and "Account already exists" in response.json().get("detail", ""):
        # Si ya existe, recuperar la cuenta para reutilizarla
        return client.get(f"/api/v1/accounts/{user_id}")
    else:
        raise Exception(f"Failed to create or retrieve account: {response.json()}")

@pytest.fixture
def authenticate():
    email = "usernew2@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username":email, "password":password})
    return response.json()['access_token']


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
        "id": str(account_id)
    }
    response = client.post("api/v1/accounts/", json=account_data)
    assert response.status_code == 400

def test_get_account_me(authenticate, create_account2):
    # Obtener la cuenta actual
    headers = {"Authorization": f"Bearer {authenticate}"}
    response = client.get("/api/v1/accounts/me", headers=headers)
    assert response.status_code == 200
    assert response.json()['id'] == create_account2.json()['id']

def test_get_account_by_id(create_account2, authenticate):
    # Obtener una cuenta específica por ID
    headers = {"Authorization": f"Bearer {authenticate}"}
    account_id = create_account2.json()['id']
    response = client.get(f"/api/v1/accounts/{account_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == account_id

def test_get_accounts(authenticate):
    # Obtener todas las cuentas
    headers = {"Authorization": f"Bearer {authenticate}"}
    response = client.get("/api/v1/accounts/", headers=headers)
    assert response.status_code == 200
    assert "data" in response.json()
    assert "count" in response.json()

def test_update_account_me(create_account2, authenticate):
    # Actualizar datos de la cuenta propia
    headers = {"Authorization": f"Bearer {authenticate}"}
    account_update_data = {"bio": "new_value"}
    response = client.patch("/api/v1/accounts/me", json=account_update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["bio"] == "new_value"

def test_update_account_by_id(create_account2, authenticate_super, create_account_super):
    # Actualizar una cuenta específica por ID
    headers = {"Authorization": f"Bearer {authenticate_super}"}
    account_id = create_account2.json()['id']
    account_update_data = {"bio": "updated_value"}
    response = client.patch(f"/api/v1/accounts/{account_id}", json=account_update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["bio"] == "updated_value"

def test_delete_account_me(create_account2, authenticate):
    # Eliminar la cuenta actual
    headers = {"Authorization": f"Bearer {authenticate}"}
    response = client.delete("/api/v1/accounts/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Account deleted successfully"


def test_delete_account_by_id(create_account3, authenticate_super, create_account_super):
    # Eliminar una cuenta específica por ID
    headers = {"Authorization": f"Bearer {authenticate_super}"}
    account_id = create_account3.json()['id']
    response = client.delete(f"/api/v1/accounts/{account_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Account deleted successfully"

def test_get_account_not_found():
    # Obtener una cuenta inexistente
    non_existing_account_id = uuid4()
    response = client.get(f"/api/v1/accounts/{non_existing_account_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Account not found"