from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app import crud
from app.models import (Account, AccountBase, User, UserCreate, AccountUpdate, Follower)
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
import pytest

created_account_data = {}

@pytest.fixture
def create_user1(db: Session):
    email = "test1@example.com"
    password = "password123"
    name = "John"
    surname = "Doe"
    is_editor = False

    user_in = UserCreate(email=email, password=password,is_editor=is_editor, name=name,surname=surname)
    user = crud.user.create_user(session=db, user_create=user_in)

    return user

@pytest.fixture
def create_account1(db: Session, create_user1):
    user_in = create_user1

    account_in = Account(id=user_in.id)
    account = crud.account.create_account(session=db, account=account_in)

    created_account_data["account1"] = account

    return account, user_in

@pytest.fixture
def create_user2(db: Session):
    email = "test2@example.com"
    password = "password123"
    name = "Test"
    surname = "Doe"
    is_editor = False

    user_in = UserCreate(email=email, password=password,is_editor=is_editor, name=name,surname=surname)
    user = crud.user.create_user(session=db, user_create=user_in)

    return user

@pytest.fixture
def create_account2(db: Session, create_user2):
    user_in = create_user2

    account_in = Account(id=user_in.id)
    account = crud.account.create_account(session=db, account=account_in)

    created_account_data["account2"] = account

    return account, user_in


def test_create_follow(db: Session, create_account1, create_account2):
    """Prueba la creación de un seguimiento."""
    _, current_user = create_account2
    account, _ = create_account1

    # Crear un follow
    new_follower = crud.follower.create_follow(session=db, account=account, current_user=current_user)

    # Verificar que el follower fue creado
    assert new_follower.follower_id == current_user.account.id
    assert new_follower.following_id == account.id

    # Verificar que las métricas se actualizaron correctamente
    assert account.num_followers == 1
    assert current_user.account.num_following == 1

def test_delete_follow(db: Session):
    """Prueba la eliminación de un seguimiento."""
    user1 = created_account_data["account1"].user
    account2 = created_account_data["account2"]

    # Crear un follow
    new_follower = crud.follower.create_follow(session=db, account=account2, current_user=user1)

    # Eliminar el follow
    crud.follower.delete_follow(session=db, account=account2, current_user=user1, follow=new_follower)

    # Verificar que las métricas se actualizaron correctamente
    assert account2.num_followers == 0
    assert user1.account.num_following == 0

    # Verificar que el follower fue eliminado
    follow_in_db = db.query(Follower).filter_by(follower_id=user1.account.id, following_id=account2.id).first()
    assert follow_in_db is None