import uuid
from datetime import datetime, timedelta, timezone

import jwt
import pytest

from app.core.security import DUMMY_HASH
from app.core.settings import settings
from app.db.models.user import User


def test_authenticate_user_returns_user(mocker, mock_auth_repository, auth_service):
    mock_user = User()
    mock_auth_repository.get_user_by_identifier.return_value = mock_user
    mocker.patch("app.services.auth.verify_password", return_value=True)

    user = auth_service.authenticate_user("identifier", "password")

    assert user == mock_user


def test_authenticate_user_returns_none_when_identifier_is_empty(auth_service):
    result = auth_service.authenticate_user("", "password")

    assert result is None


def test_authenticate_user_returns_none_when_password_is_empty(auth_service):
    result = auth_service.authenticate_user("identifier", "")

    assert result is None


def test_authenticate_user_returns_none_when_user_not_found(
    mock_auth_repository, auth_service
):
    mock_auth_repository.get_user_by_identifier.return_value = None

    result = auth_service.authenticate_user("identifier", "password")

    assert result is None


def test_authenticate_user_returns_none_when_password_verification_fails(
    mocker, mock_auth_repository, auth_service
):
    mock_user = User()
    mock_auth_repository.get_user_by_identifier.return_value = mock_user
    mocker.patch("app.services.auth.verify_password", return_value=False)

    result = auth_service.authenticate_user("identifier", "password")

    assert result is None


def test_authenticate_user_avoids_timing_attack(
    mocker, mock_auth_repository, auth_service
):
    mock_auth_repository.get_user_by_identifier.return_value = None
    mock_verify_password = mocker.patch("app.services.auth.verify_password")

    auth_service.authenticate_user("identifier", "password")

    mock_verify_password.assert_called_once_with("password", DUMMY_HASH)


@pytest.mark.parametrize("token_kind", ["access", "refresh"])
def tests_create_token_success(auth_service, token_kind):
    data = {"sub": "user_id"}
    encoded_jwt, expire, jti = auth_service.create_token(
        data=data, token_kind=token_kind
    )

    payload = jwt.decode(
        encoded_jwt, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    # Get the current time for comparison
    now = datetime.now(timezone.utc)

    # Allow small time difference because datetime.now() is called in both token creation (source) and test execution
    delta = timedelta(seconds=5)

    # Convert "exp" and "iat" in payload from timestamp to datetime for easier assertions
    exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    iat = datetime.fromtimestamp(payload["iat"], tz=timezone.utc)

    assert payload["type"] == token_kind
    assert payload["sub"] == data["sub"]
    assert exp > now
    assert now - delta <= iat <= now + delta
    assert expire > now

    if token_kind == "access":
        assert "jti" not in payload
        assert jti is None
    elif token_kind == "refresh":
        assert "jti" in payload
        assert payload["jti"] == str(jti)
        assert isinstance(jti, uuid.UUID)


@pytest.mark.parametrize("token_kind", ["access", "refresh"])
def test_create_token_with_expires_delta_as_argument(auth_service, token_kind):
    data = {"sub": "user_id"}
    expires_delta = timedelta(minutes=10)

    encoded_jwt, expire, jti = auth_service.create_token(
        data=data, token_kind=token_kind, expires_delta=expires_delta
    )

    now = datetime.now(timezone.utc)

    assert encoded_jwt is not None
    assert expire is not None
    assert expire > now

    if token_kind == "access":
        assert jti is None
    elif token_kind == "refresh":
        assert jti is not None


def test_create_token_with_invalid_token_kind(auth_service):
    data = {"sub": "user_id"}

    with pytest.raises(ValueError, match="Invalid token kind"):
        auth_service.create_token(data=data, token_kind="invalid_kind")
