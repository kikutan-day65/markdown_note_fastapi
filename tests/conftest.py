import pytest

from app.services.auth import AuthService


@pytest.fixture
def mock_auth_repository(mocker):
    return mocker.Mock()


@pytest.fixture
def auth_service(mock_auth_repository):
    return AuthService(repository=mock_auth_repository)
