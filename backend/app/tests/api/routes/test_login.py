from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string
import pytest
import jwt
from app.core.config import settings

client = TestClient(app)

@pytest.fixture
def create_user():
    user_data = {
        "email": "newuser5@example.com",
        "password": "password123",
        "name": "new",
        "surname" :"user",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response

def test_authenticate(create_user):
    email = "newuser5@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username":email, "password":password})
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["access_token"] is not None

    decoded_token = jwt.decode(
        response.json()["access_token"],
        settings.SECRET_KEY,
        algorithms=["HS256"]
    )
    

    assert decoded_token["sub"] == str(create_user.json()["id"])


def test_authenticate_failed_wrong_email():
    email = "newuser90@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username":email, "password":password})
    assert response.status_code == 400
    json_response = response.json()
    assert json_response["detail"] == "Incorrect email or password"


def test_authenticate_failed_wrong_email():
    email = "newuser5@example.com"
    password = "password12"

    response = client.post("/api/v1/login/access-token/", data={"username":email, "password":password})
    assert response.status_code == 400
    json_response = response.json()
    assert json_response["detail"] == "Incorrect email or password"
