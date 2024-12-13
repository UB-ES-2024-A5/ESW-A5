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