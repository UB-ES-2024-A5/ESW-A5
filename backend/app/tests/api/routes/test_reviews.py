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
created_account_data_review = {}

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

    created_account_data_review["account1"] = response.json()

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

    created_account_data_review["account2"] = response.json()

    return response
@pytest.fixture
def authenticate2():
    email = "userreview2@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username": email, "password": password})
    return response.json()['access_token']

@pytest.fixture
def create_user_editor():
    user_data = {
        "email": "editorreview1@example.com",
        "password": "password123",
        "name": "Editor1",
        "cif" :"g11116666",
        "is_editor": True
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response

@pytest.fixture
def create_account_editor(create_user_editor):
    user_out = create_user_editor.json()
    user_id = user_out['id']
    account_data = {
        "id": user_id
    }

    response = client.post("/api/v1/accounts/", json=account_data)

    created_account_data_review["account_editor"] = response.json()

    return response
@pytest.fixture
def authenticate_editor():
    email = "editorreview1@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username":email, "password":password})
    return response.json()['access_token']

@pytest.fixture
def create_user_editor2():
    user_data = {
        "email": "editorreview2@example.com",
        "password": "password123",
        "name": "Editor2",
        "cif" :"g77777777",
        "is_editor": True
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response

@pytest.fixture
def create_account_editor2(create_user_editor2):
    user_out = create_user_editor2.json()
    user_id = user_out['id']
    account_data = {
        "id": user_id
    }

    response = client.post("/api/v1/accounts/", json=account_data)

    created_account_data_review["account_editor2"] = response.json()

    return response
@pytest.fixture
def authenticate_editor2():
    email = "editorreview2@example.com"
    password = "password123"

    response = client.post("/api/v1/login/access-token/", data={"username":email, "password":password})
    return response.json()['access_token']

@pytest.fixture
def create_book1(authenticate_editor):
    account = client.get("/api/v1/users/by_email/editorreview1@example.com")
    account_id = account.json()['id']
    book_data = {
        "title" : "El imperio final",
        "author" : "Brandon Sanderson",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "9788498726138",
        "account_id" : account_id,
        "price" : 12.30,
        "publication_year" : 2020,
        "links": ["https://www.casadellibro.com/libro-el-imperio-final-saga-nacidos-de-la-bruma-1/9788498726138/1956329"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate_editor}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)

    created_account_data_review["book1"] = response.json()

    return response

@pytest.fixture
def create_book2(authenticate_editor):
    account = client.get("/api/v1/users/by_email/editorreview1@example.com")
    account_id = account.json()['id']
    book_data = {
        "title" : "El pozo de la ascension",
        "author" : "Brandon Sanderson",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "9788418037276",
        "account_id" : account_id,
        "price" : 28.40,
        "publication_year" : 2021,
        "links": ["https://www.casadellibro.com/libro-el-pozo-de-la-ascension-nacidos-de-la-bruma-mistborn-edicion-ilustrada-2/9788418037276/12382307"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate_editor}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)

    created_account_data_review["book2"] = response.json()

    return response

@pytest.fixture
def create_book3(authenticate_editor):
    account = client.get("/api/v1/users/by_email/editorreview1@example.com")
    account_id = account.json()['id']
    book_data = {
        "title" : "El heroe de las eras",
        "author" : "Brandon Sanderson",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "9788466658911",
        "account_id" : account_id,
        "price" : 23.65,
        "publication_year" : 2016,
        "links": ["https://www.casadellibro.com/libro-el-heroe-de-las-eras-saga-nacidos-de-la-bruma-3/9788466658911/3082061"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate_editor}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)

    created_account_data_review["book3"] = response.json()

    return response

@pytest.fixture
def create_book4(authenticate_editor2):
    account = client.get("/api/v1/users/by_email/editorreview2@example.com")
    account_id = account.json()['id']
    book_data = {
        "title" : "Aleacion de ley",
        "author" : "Brandon Sanderson",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "9788466658928",
        "account_id" : account_id,
        "price" : 23.65,
        "publication_year" : 2016,
        "links": ["https://www.casadellibro.com/libro-aleacion-de-ley-saga-nacidos-de-la-bruma-4/9788466658928/3082062"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate_editor2}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)

    created_account_data_review["book4"] = response.json()

    return response

@pytest.fixture
def create_book5(authenticate_editor2):
    account = client.get("/api/v1/users/by_email/editorreview2@example.com")
    account_id = account.json()['id']
    book_data = {
        "title" : "Sombras de identidad",
        "author" : "Brandon Sanderson",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "9788466658850",
        "account_id" : account_id,
        "price" : 23.65,
        "publication_year" : 2016,
        "links": ["https://www.casadellibro.com/libro-sombras-de-identidad-saga-nacidos-de-la-bruma-5/9788466658850/3082063"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate_editor2}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)

    created_account_data_review["book5"] = response.json()

    return response

@pytest.fixture
def create_book6(authenticate_editor2):
    account = client.get("/api/v1/users/by_email/editorreview2@example.com")
    account_id = account.json()['id']
    book_data = {
        "title" : "Brazales de duelo",
        "author" : "Brandon Sanderson",
        "gender_main" : "Fantasia",
        "synopsis" : "lorem ipsum",
        "isbn" : "9788466659628",
        "account_id" : account_id,
        "price" : 23.65,
        "publication_year" : 2016,
        "links": ["https://www.casadellibro.com/libro-brazales-de-duelo-saga-nacidos-de-la-bruma-6/9788466659628/5420146"]
    }

    headers = {
        "Authorization": f"Bearer {authenticate_editor2}"
    }

    response = client.post("/api/v1/books/", json=book_data, headers=headers)

    created_account_data_review["book6"] = response.json()

    return response


def test_create_review_point_book(create_account, create_account2, create_account_editor, create_account_editor2,
                                  create_book1, create_book2, create_book3, create_book4, create_book5, create_book6,
                                  authenticate):
    """
    Comprobamos la creacion de una review con post
    """

    book_id = created_account_data_review["book1"]["id"]

    review_data = {
        "point_book": 3
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post(f"/api/v1/reviews/point_book/{book_id}", json=review_data, headers=headers)
    assert response.status_code == 200
    results = response.json()
    assert review_data['point_book'] == results["point_book"]
    assert len(results["list_comments"]) == 0

def test_create_review_point_book_duplicate(authenticate):
    """
    Comprobamos el error de una review duplicada
    """

    book_id = created_account_data_review["book1"]["id"]

    review_data = {
        "point_book": 3
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.post(f"/api/v1/reviews/point_book/{book_id}", json=review_data, headers=headers)
    assert response.status_code == 400
    results = response.json()
    assert results['detail'] == "Review already exists."

def test_create_review_point_book_being_editor(authenticate_editor):
    """
    Comprobamos el error de intentar publicar una review siendo editor
    """

    book_id = created_account_data_review["book1"]["id"]

    review_data = {
        "point_book": 3
    }

    headers = {
        "Authorization": f"Bearer {authenticate_editor}"
    }

    response = client.post(f"/api/v1/reviews/point_book/{book_id}", json=review_data, headers=headers)
    assert response.status_code == 400
    results = response.json()

    assert results['detail'] == "The user cannot be an editorial user."

def test_update_review_point_book_not_found(authenticate):
    """
    Comprobamos el error de una review no encontrada
    """

    book_id = created_account_data_review["book2"]["id"]

    review_data = {
        "point_book": 3
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.patch(f"/api/v1/reviews/point_book/{book_id}", json=review_data, headers=headers)
    assert response.status_code == 400
    results = response.json()

    assert results['detail'] == "Review not found."

def test_update_review_point_book(authenticate):
    """
    Comprobamos la actualizacion del pb
    """

    book_id = created_account_data_review["book1"]["id"]

    review_data = {
        "point_book": 4
    }

    headers = {
        "Authorization": f"Bearer {authenticate}"
    }

    response = client.patch(f"/api/v1/reviews/point_book/{book_id}", json=review_data, headers=headers)
    assert response.status_code == 200
    results = response.json()

    assert review_data['point_book'] == results["point_book"]
    assert len(results["list_comments"]) == 0

def test_create_review_pb_put(authenticate2):
    """
    Comprobamos la creacion de un pb con el metodo put
    """
    book_id = created_account_data_review["book1"]["id"]

    review_data = {
        "point_book": 4
    }

    headers = {
        "Authorization": f"Bearer {authenticate2}"
    }

    response = client.put(f"/api/v1/reviews/point_book/{book_id}", json=review_data, headers=headers)
    assert response.status_code == 200
    results = response.json()

    assert review_data['point_book'] == results["point_book"]
    assert len(results["list_comments"]) == 0

def test_update_review_pb_put(authenticate2):
    """
    Comprobamos que se actualiza el pb de un comment con el metodo put
    """
    book_id = created_account_data_review["book1"]["id"]

    review_data = {
        "point_book": 1
    }

    headers = {
        "Authorization": f"Bearer {authenticate2}"
    }

    response = client.put(f"/api/v1/reviews/point_book/{book_id}", json=review_data, headers=headers)
    assert response.status_code == 200
    results = response.json()

    assert review_data['point_book'] == results["point_book"]
    assert len(results["list_comments"]) == 0

def test_create_comment(authenticate2):
    """
    Comprobamos la creacion de un comment
    """
    book_id = created_account_data_review["book2"]["id"]

    review_data = {
        "text": "creo un comment"
    }

    headers = {
        "Authorization": f"Bearer {authenticate2}"
    }

    response = client.post(f"/api/v1/reviews/comment/{book_id}", json=review_data, headers=headers)
    assert response.status_code == 200
    results = response.json()

    assert len(results["list_comments"]) == 1

    comment_texts = {comment for comment in results["list_comments"]}
    assert review_data["text"] in comment_texts

def test_create_comment_duplicate(authenticate2):
    """
    Comprobamos el mensaje de error si ya existe el comment
    """
    book_id = created_account_data_review["book2"]["id"]

    review_data = {
        "text": "creo un comment 2"
    }

    headers = {
        "Authorization": f"Bearer {authenticate2}"
    }

    response = client.post(f"/api/v1/reviews/comment/{book_id}", json=review_data, headers=headers)
    assert response.status_code == 400
    results = response.json()

    assert results["detail"] == "Review already exists."

def test_create_review_pb_put_with_comment(authenticate2):
    """
    Comprobamos que se crea bien el pb cuando solamente existe un comentario
    """
    book_id = created_account_data_review["book2"]["id"]

    review_data = {
        "point_book": 2
    }

    headers = {
        "Authorization": f"Bearer {authenticate2}"
    }

    response = client.put(f"/api/v1/reviews/point_book/{book_id}", json=review_data, headers=headers)
    assert response.status_code == 200
    results = response.json()

    assert review_data['point_book'] == results["point_book"]
    assert len(results["list_comments"]) == 1
    comment_texts = {comment for comment in results["list_comments"]}
    assert "creo un comment" in comment_texts

def test_update_review_pb_put_with_comment(authenticate2):
    """
    Comprobamos que se actualiza correctamente el pb pese ya haber un pb y un comment
    """

    book_id = created_account_data_review["book2"]["id"]

    review_data = {
        "point_book": 4
    }

    headers = {
        "Authorization": f"Bearer {authenticate2}"
    }

    response = client.put(f"/api/v1/reviews/point_book/{book_id}", json=review_data, headers=headers)
    assert response.status_code == 200
    results = response.json()

    assert review_data['point_book'] == results["point_book"]
    assert len(results["list_comments"]) == 1
    comment_texts = {comment for comment in results["list_comments"]}
    assert "creo un comment" in comment_texts



