""" Tests configuration module """

import os
if "GITHUB_ACTIONS" not in os.environ:
    os.environ["ENVIRONMENT"] = "testing"


from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.config import settings
from app.core.db import engine, init_db
from app.main import app
from app.models import User, Account, Link, Book, WishList, WishlistBookLink
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers




@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            init_db(session)
            yield session
        finally:
            session.rollback()
            session.exec(delete(WishlistBookLink))
            session.exec(delete(WishList))
            session.exec(delete(Link))
            session.exec(delete(Book))
            session.exec(delete(Account))
            session.exec(delete(User))
            session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
