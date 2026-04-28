from unittest.mock import Mock

import pytest

from app.repositories.auth import AuthRepository
from app.services.auth import AuthService


@pytest.fixture
def mock_auth_repository():
    return Mock(spec=AuthRepository)


@pytest.fixture
def auth_service(mock_auth_repository):
    return AuthService(repository=mock_auth_repository)


class DummyFormData:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


@pytest.fixture
def dummy_form_data():
    return DummyFormData(username="testuser", password="password123")
