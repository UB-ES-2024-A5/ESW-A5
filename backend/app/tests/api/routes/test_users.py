from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlmodel import Session
from app.main import app
from app import crud
from app.core.config import settings
from app.models import UserCreate
from app.tests.utils.utils import random_email, random_lower_string

client = TestClient(app)

def test_create_user():
    user_data = {
        "email": "newuser@example.com",
        "password": "password123",
        "name": "new",
        "surname" :"user",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]

def test_create_editorial():
    editorial_data = {
        "email" : "editorial@example.com",
        "password" : "password",
        "name" : "Vaixell de Vapor",
        "cif" : "G66458933",
        "is_editor" : True
    }
    response = client.post("api/v1/users/", json=editorial_data)
    assert response.status_code == 200
    assert response.json()["email"] == editorial_data["email"]
    assert response.json()["cif"] == editorial_data["cif"]

def test_duplicate_user():
    user_data = {
        "email": "newuser@example.com",
        "password": "password123",
        "name": "perico",
        "surname" :"palotes",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400
    assert response.json()['detail'] == "The user with this email already exists in the system."

def test_duplicate_editorial_email():
    editorial_data = {
        "email" : "editorial@example.com",
        "password" : "password",
        "name" : "Vaixell de Vapor",
        "cif" : "G66458932",
        "is_editor" : True
    }
    response = client.post("/api/v1/users/", json=editorial_data)
    assert response.status_code == 400
    assert response.json()['detail'] == "The user with this email already exists in the system."

def test_duplicate_editorial_cif():
    editorial_data = {
        "email" : "editorial2@example.com",
        "password" : "password",
        "name" : "Vaixell de Vapor",
        "cif" : "G66458933",
        "is_editor" : True
    }
    response = client.post("/api/v1/users/", json=editorial_data)
    assert response.status_code == 400
    assert response.json()['detail'] == "The editorial with this CIF already exists in the system."

def test_less_8char_password():
    user_data = {
        "email": "newuser2@example.com",
        "password": "p",
        "name": "perico",
        "surname" :"palotes",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 422

def test_40char_password():
    user_data = {
        "email": "newuser3@example.com",
        "password": "pppppppppppppppppppppppppppppppppppppppp",
        "name": "perico",
        "surname" :"palotes",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]

def test_more_40char_password():
    user_data = {
        "email": "newuser4@example.com",
        "password": "ppppppppppppppppppppppppppppppppppppppppp",
        "name": "perico",
        "surname" :"palotes",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 422

def test_mail_invalid():
    user_data = {
        "email": "newuser5.com",
        "password": "papapapapa",
        "name": "perico",
        "surname" :"palotes",
        "is_editor": False
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 422


"""   
def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_create_user_new_email(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    with patch("app.utils.send_email", return_value=None), patch(
        "app.core.config.settings.SMTP_HOST", "smtp.example.com"
    ), patch("app.core.config.settings.SMTP_USER", "admin@example.com"):
        username = random_email()
        password = random_lower_string()
        data = {"email": username, "password": password}
        r = client.post(
            f"{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=data,
        )
        assert 200 <= r.status_code < 300
        created_user = r.json()
        user = crud.user.get_user_by_email(session=db, email=username)
        assert user
        assert user.email == created_user["email"]


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create_user(session=db, user_create=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_user_by_email(session=db, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_get_existing_user_current_user(client: TestClient, db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create_user(session=db, user_create=user_in)
    user_id = user.id

    login_data = {
        "username": username,
        "password": password,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_user_by_email(session=db, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_get_existing_user_permissions_error(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/999999",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403
    assert r.json() == {"detail": "The user doesn't have enough privileges"}


def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    # username = email
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create_user(session=db, user_create=user_in)
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_retrieve_users(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create_user(session=db, user_create=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    crud.user.create_user(session=db, user_create=user_in2)

    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users["data"]) > 1
    assert "count" in all_users
    for item in all_users["data"]:
        assert "email" in item


def test_update_user_me(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    full_name = "Updated Name"
    email = random_email()
    data = {"full_name": full_name, "email": email}
    r = client.patch(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_user = r.json()
    assert updated_user["email"] == email
    assert updated_user["full_name"] == full_name


def test_update_password_me(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    new_password = random_lower_string()
    data = {
        "current_password": settings.FIRST_SUPERUSER_PASSWORD,
        "new_password": new_password,
    }
    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_user = r.json()
    assert updated_user["message"] == "Password updated successfully"

    # Revert to the old password to keep consistency in test
    old_data = {
        "current_password": new_password,
        "new_password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=superuser_token_headers,
        json=old_data,
    )
    assert r.status_code == 200


def test_update_password_me_incorrect_password(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    new_password = random_lower_string()
    data = {"current_password": new_password, "new_password": new_password}
    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 400
    updated_user = r.json()
    assert updated_user["detail"] == "Incorrect password"


def test_update_user_me_email_exists(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create_user(session=db, user_create=user_in)

    data = {"email": user.email}
    r = client.patch(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "User with this email already exists"


def test_update_password_me_same_password_error(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    data = {
        "current_password": settings.FIRST_SUPERUSER_PASSWORD,
        "new_password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 400
    updated_user = r.json()
    assert (
        updated_user["detail"] == "New password cannot be the same as the current one"
    )


def test_create_user_open(client: TestClient) -> None:
    with patch("app.core.config.settings.USERS_OPEN_REGISTRATION", True):
        username = random_email()
        password = random_lower_string()
        full_name = random_lower_string()
        data = {"email": username, "password": password, "full_name": full_name}
        r = client.post(
            f"{settings.API_V1_STR}/users/open",
            json=data,
        )
        assert r.status_code == 200
        created_user = r.json()
        assert created_user["email"] == username
        assert created_user["full_name"] == full_name


def test_create_user_open_forbidden_error(client: TestClient) -> None:
    with patch("app.core.config.settings.USERS_OPEN_REGISTRATION", False):
        username = random_email()
        password = random_lower_string()
        full_name = random_lower_string()
        data = {"email": username, "password": password, "full_name": full_name}
        r = client.post(
            f"{settings.API_V1_STR}/users/open",
            json=data,
        )
        assert r.status_code == 403
        assert (
            r.json()["detail"] == "Open user registration is forbidden on this server"
        )


def test_create_user_open_already_exists_error(client: TestClient) -> None:
    with patch("app.core.config.settings.USERS_OPEN_REGISTRATION", True):
        password = random_lower_string()
        full_name = random_lower_string()
        data = {
            "email": settings.FIRST_SUPERUSER,
            "password": password,
            "full_name": full_name,
        }
        r = client.post(
            f"{settings.API_V1_STR}/users/open",
            json=data,
        )
        assert r.status_code == 400
        assert (
            r.json()["detail"]
            == "The user with this email already exists in the system"
        )


def test_update_user(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create_user(session=db, user_create=user_in)

    data = {"full_name": "Updated_full_name"}
    r = client.patch(
        f"{settings.API_V1_STR}/users/{user.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_user = r.json()
    assert updated_user["full_name"] == "Updated_full_name"


def test_update_user_not_exists(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    data = {"full_name": "Updated_full_name"}
    r = client.patch(
        f"{settings.API_V1_STR}/users/99999999",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "The user with this id does not exist in the system"


def test_update_user_email_exists(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create_user(session=db, user_create=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    user2 = crud.user.create_user(session=db, user_create=user_in2)

    data = {"email": user2.email}
    r = client.patch(
        f"{settings.API_V1_STR}/users/{user.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "User with this email already exists"


def test_delete_user_super_user(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create_user(session=db, user_create=user_in)
    user_id = user.id
    r = client.delete(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    deleted_user = r.json()
    assert deleted_user["message"] == "User deleted successfully"


def test_delete_user_current_user(client: TestClient, db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create_user(session=db, user_create=user_in)
    user_id = user.id

    login_data = {
        "username": username,
        "password": password,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    r = client.delete(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=headers,
    )
    assert r.status_code == 200
    deleted_user = r.json()
    assert deleted_user["message"] == "User deleted successfully"


def test_delete_user_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    r = client.delete(
        f"{settings.API_V1_STR}/users/99999999",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "User not found"


def test_delete_user_current_super_user_error(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    super_user = crud.user.get_user_by_email(session=db, email=settings.FIRST_SUPERUSER)
    assert super_user
    user_id = super_user.id

    r = client.delete(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "Super users are not allowed to delete themselves"


def test_delete_user_without_privileges(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create_user(session=db, user_create=user_in)

    r = client.delete(
        f"{settings.API_V1_STR}/users/{user.id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "The user doesn't have enough privileges"
"""