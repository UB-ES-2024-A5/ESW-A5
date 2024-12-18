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

# Variable para almacenar datos entre pruebas
created_account_data_forum = {}

@pytest.fixture
def create_user():
    user_data = {
        "email": "userforum1@example.com",
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

    created_account_data_forum["account1"] = response.json()

    return response


@pytest.fixture
def authenticate():
    email = "userforum1@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username": email, "password": password})
    return response.json()['access_token']


@pytest.fixture
def create_user2():
    user_data = {
        "email": "userforum2@example.com",
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

    created_account_data_forum["account2"] = response.json()

    return response


@pytest.fixture
def authenticate2():
    email = "userforum2@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username": email, "password": password})
    return response.json()['access_token']


@pytest.fixture
def create_follower(create_account, create_account2, authenticate):
    account1_id = created_account_data_forum["account1"]['id']
    account2_id = created_account_data_forum["account2"]['id']

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post(f"/api/v1/followers/{account2_id}", headers=headers)

    created_account_data_forum["follower1"] = response.json()

    return response


def test_create_post(create_follower, authenticate):
    account1_id = created_account_data_forum["account1"]['id']

    forum_data = {
        "text": "primer post"
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post(f"/api/v1/forums/", json=forum_data, headers=headers)

    created_account_data_forum["post1"] = response.json()

    assert response.status_code == 200
    results = response.json()

    assert results["text"] == forum_data["text"]
    assert account1_id == results["account_id"]


def test_create_response_without_parent(authenticate):
    account1_id = created_account_data_forum["account1"]['id']
    parent_id = uuid4()

    forum_data = {
        "text": "primera response"
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post(f"/api/v1/forums/{parent_id}", json=forum_data, headers=headers)

    assert response.status_code == 404
    results = response.json()

    assert results["detail"] == "Parent post does not exist"


def test_create_response(authenticate2):
    parent_id = created_account_data_forum["post1"]["id"]

    forum_data = {
        "text": "primera response"
    }

    headers = {
        "Authorization": f"Bearer {authenticate2}"
    }

    response = client.post(f"/api/v1/forums/{parent_id}", json=forum_data, headers=headers)

    assert response.status_code == 200
    results = response.json()

    created_account_data_forum["response1_1"] = results

    assert results["text"] == forum_data["text"]
    assert results["parent_forum_id"] == parent_id


def test_get_all_my_posts(authenticate, authenticate2):
    forum_data = {
        "text": "segundo post"
    }

    headers = {
        "Authorization": f"Bearer {authenticate2}"
    }

    response = client.post(f"/api/v1/forums/", json=forum_data, headers=headers)

    created_account_data_forum["post2"] = response.json()

    response = client.get(f"api/v1/forums/all_posts_me/", headers=headers)

    assert response.status_code == 200
    results = response.json()

    assert results["count"] == 2

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.get(f"api/v1/forums/all_posts_me/", headers=headers)

    assert response.status_code == 200
    results = response.json()

    assert results["count"] == 1


def test_get_posts_responses_by_account_id():
    account1_id = created_account_data_forum["account1"]['id']
    account2_id = created_account_data_forum["account2"]['id']

    response = client.get(f"api/v1/forums/all_posts/{account1_id}")

    assert response.status_code == 200
    results = response.json()
    assert results["count"] == 1

    response = client.get(f"api/v1/forums/all_posts/{account2_id}")

    assert response.status_code == 200
    results = response.json()
    assert results["count"] == 2

def test_get_post_by_id_non_existent():
    post_id = uuid4()

    response = client.get(f"api/v1/forums/post_by_id/{post_id}")

    assert response.status_code == 404
    results = response.json()
    assert results["detail"] == "Post does not exist"


def test_get_post_by_id():
    post_id = created_account_data_forum["post1"]["id"]

    response = client.get(f"api/v1/forums/post_by_id/{post_id}")

    assert response.status_code == 200
    results = response.json()
    assert results["text"] == "primer post"


def test_get_posts_following(authenticate):
    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.get(f"/api/v1/forums/all_post_my_following/", headers=headers)

    assert response.status_code == 200
    results = response.json()
    assert results["count"] == 1


def test_get_responses_by_post_non_existent():
    post_id = uuid4()

    response = client.get(f"/api/v1/forums/responses/{post_id}")

    assert response.status_code == 404
    results = response.json()
    assert results["detail"] == "Post does not exist"


def test_get_responses_by_post():
    post_id = created_account_data_forum["post1"]["id"]

    response = client.get(f"/api/v1/forums/responses/{post_id}")

    assert response.status_code == 200
    results = response.json()
    assert results["count"] == 1


def test_create_reaction_non_existent_post(authenticate):
    post_id = uuid4()

    reaction_data = {
        "type": True
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post(f"/api/v1/forums/create_reaction/{post_id}", json=reaction_data, headers=headers)

    assert response.status_code == 404
    results = response.json()
    assert results["detail"] == "Post Forum does not exist"


def test_create_reaction(authenticate):
    post_id = created_account_data_forum["post1"]["id"]

    reaction_data = {
        "type": True
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post(f"/api/v1/forums/create_reaction/{post_id}", json=reaction_data, headers=headers)

    assert response.status_code == 200
    results = response.json()
    assert results["type"] == reaction_data["type"]


def test_create_reaction_duplicate(authenticate):
    post_id = created_account_data_forum["post1"]["id"]

    reaction_data = {
        "type": True
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post(f"/api/v1/forums/create_reaction/{post_id}", json=reaction_data, headers=headers)

    assert response.status_code == 400
    results = response.json()
    assert results["detail"] == "Reaction already exists."



def test_update_reaction_post_not_found(authenticate):
    post_id = uuid4()

    reaction_data = {
        "type": False
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.patch(f"/api/v1/forums/update_reaction/{post_id}", json=reaction_data, headers=headers)

    assert response.status_code == 404
    results = response.json()
    assert results["detail"] == "Post Forum does not exist"


def test_update_reaction_not_found(authenticate2):
    post_id = created_account_data_forum["post1"]["id"]

    reaction_data = {
        "type": False
    }

    headers = {
        "Authorization": f"Bearer {authenticate2}"
    }

    response = client.patch(f"/api/v1/forums/update_reaction/{post_id}", json=reaction_data, headers=headers)

    assert response.status_code == 400
    results = response.json()
    assert results["detail"] == "Reaction does not exists."


def test_update_reaction(authenticate):
    post_id = created_account_data_forum["post1"]["id"]

    reaction_data = {
        "type": False
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.patch(f"/api/v1/forums/update_reaction/{post_id}", json=reaction_data, headers=headers)

    assert response.status_code == 200
    results = response.json()
    assert results["type"] == reaction_data["type"]


def test_get_posts_my_like(authenticate):
    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.get(f"/api/v1/forums/posts_me_like/", headers=headers)

    assert response.status_code == 200
    results = response.json()
    assert results["count"] == 0


def test_get_posts_my_dislike(authenticate):
    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.get(f"/api/v1/forums/posts_me_dislike/", headers=headers)

    assert response.status_code == 200
    results = response.json()
    assert results["count"] == 1


def test_get_posts_account_like():
    account_id = created_account_data_forum["account1"]["id"]

    response = client.get(f"/api/v1/forums/posts_like/{account_id}/")

    assert response.status_code == 200
    results = response.json()
    assert results["count"] == 0


def test_get_posts_account_like_not_found():
    account_id = uuid4()

    response = client.get(f"/api/v1/forums/posts_like/{account_id}/")

    assert response.status_code == 404
    results = response.json()
    assert results["detail"] == "Account does not exist"


def test_get_posts_account_dislike_not_found():
    account_id = uuid4()

    response = client.get(f"/api/v1/forums/posts_dislike/{account_id}/")

    assert response.status_code == 404
    results = response.json()
    assert results["detail"] == "Account does not exist"


def test_get_posts_account_dislike():
    account_id = created_account_data_forum["account1"]["id"]

    response = client.get(f"/api/v1/forums/posts_dislike/{account_id}/")

    assert response.status_code == 200
    results = response.json()
    assert results["count"] == 1


def test_delete_reaction_not_found_post(authenticate):
    post_id = uuid4()

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.delete(f"/api/v1/forums/delete_reaction/{post_id}", headers=headers)

    assert response.status_code == 404
    results = response.json()
    assert results["detail"] == "Post Forum does not exist"


def test_delete_reaction_non_existent(authenticate2):
    post_id = created_account_data_forum["post2"]["id"]

    headers = {
        "Authorization": f"Bearer {authenticate2}"
    }

    response = client.delete(f"/api/v1/forums/delete_reaction/{post_id}", headers=headers)

    assert response.status_code == 400
    results = response.json()
    assert results["detail"] == "Reaction does not exists."


def test_delete_reaction(authenticate):
    post_id = created_account_data_forum["post1"]["id"]

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.delete(f"/api/v1/forums/delete_reaction/{post_id}", headers=headers)

    assert response.status_code == 200
    results = response.json()
    assert results["message"] == "Reaction successfully removed"


def test_delete_post_not_found(authenticate):
    post_id = uuid4()

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.delete(f"/api/v1/forums/delete_post/{post_id}", headers=headers)

    assert response.status_code == 404
    results = response.json()
    assert results["detail"] == "Post forum not found"


def test_delete_post_not_belong_user(authenticate):
    post_id = created_account_data_forum["post2"]["id"]

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.delete(f"/api/v1/forums/delete_post/{post_id}", headers=headers)

    assert response.status_code == 403
    results = response.json()
    assert results["detail"] == "This post forum does not belong to your user"


def test_delete_post(authenticate):
    post_id = created_account_data_forum["post1"]["id"]

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.delete(f"/api/v1/forums/delete_post/{post_id}", headers=headers)

    assert response.status_code == 200
    results = response.json()
    assert results["message"] == "Post Forum deleted successfully"

