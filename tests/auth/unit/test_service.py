import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

import jwt
import pytest

from app.core.exceptions import (
    AuthenticationException,
    CredentialException,
    TokenReuseException,
)
from app.core.security import DUMMY_HASH
from app.core.settings import settings
from app.db.models.refresh_token import RefreshToken
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


def test_login_success(mocker, auth_service, dummy_form_data):
    mock_user = User(id=uuid.uuid4())
    mock_authenticate_user = Mock(return_value=mock_user)
    auth_service.authenticate_user = mock_authenticate_user

    mock_create_token = Mock(
        side_effect=[
            ("access_token", None, None),
            ("refresh_token", "dummy_expire", "dummy_jti"),
        ]
    )
    auth_service.create_token = mock_create_token

    mock_save_refresh_token = Mock(return_value=None)
    auth_service.save_refresh_token = mock_save_refresh_token

    token = auth_service.login(form_data=dummy_form_data)

    mock_authenticate_user.assert_called_once_with(
        dummy_form_data.username, dummy_form_data.password
    )
    assert mock_create_token.call_count == 2
    mock_create_token.assert_any_call(
        data={"sub": str(mock_user.id)}, token_kind="access"
    )
    mock_create_token.assert_any_call(
        data={"sub": str(mock_user.id)}, token_kind="refresh"
    )
    mock_save_refresh_token.assert_called_once_with(
        user_id=mock_user.id,
        token="refresh_token",
        expire="dummy_expire",
        jti="dummy_jti",
    )
    assert token.access_token == "access_token"
    assert token.refresh_token == "refresh_token"
    assert token.token_type == "bearer"


def test_login_failure(mocker, auth_service, dummy_form_data):
    mock_authenticate_user = Mock(return_value=None)
    auth_service.authenticate_user = mock_authenticate_user

    mock_create_token = Mock()
    auth_service.create_token = mock_create_token

    mock_save_refresh_token = Mock()
    auth_service.save_refresh_token = mock_save_refresh_token

    with pytest.raises(AuthenticationException):
        auth_service.login(form_data=dummy_form_data)

    mock_create_token.assert_not_called()
    mock_save_refresh_token.assert_not_called()


def test_logout_success(mocker, auth_service, mock_auth_repository):
    input_token = "dummy_token"

    mock_user_id = uuid.uuid4()
    mock_jti = uuid.uuid4()
    mock_decode_refresh_token = Mock(return_value=(mock_user_id, mock_jti))
    auth_service.decode_refresh_token = mock_decode_refresh_token

    mock_user = User(id=mock_user_id)
    mock_auth_repository.get_user_by_id.return_value = mock_user

    mock_refresh_token = RefreshToken(token="hashed_input_token", jti=mock_jti)
    mock_auth_repository.get_refresh_token_by_jti.return_value = mock_refresh_token

    mock_verify_password = mocker.patch(
        "app.services.auth.verify_password", return_value=True
    )

    mock_revoke_refresh_token = Mock()
    auth_service.revoke_refresh_token = mock_revoke_refresh_token

    auth_service.logout(token=input_token)

    mock_decode_refresh_token.assert_called_once_with(token=input_token)
    mock_auth_repository.get_user_by_id.assert_called_once_with(mock_user_id)
    mock_auth_repository.get_refresh_token_by_jti.assert_called_once_with(jti=mock_jti)
    mock_verify_password.assert_called_once_with(input_token, mock_refresh_token.token)
    mock_revoke_refresh_token.assert_called_once_with(target=mock_refresh_token)


def test_logout_fails_when_user_not_found(mocker, auth_service, mock_auth_repository):
    input_token = "dummy_token"

    mock_user_id = uuid.uuid4()
    mock_jti = uuid.uuid4()
    mock_decode_refresh_token = Mock(return_value=(mock_user_id, mock_jti))
    auth_service.decode_refresh_token = mock_decode_refresh_token

    mock_auth_repository.get_user_by_id.return_value = None

    mock_verify_password = mocker.patch("app.services.auth.verify_password")

    mock_revoke_refresh_token = Mock()
    auth_service.revoke_refresh_token = mock_revoke_refresh_token

    with pytest.raises(CredentialException):
        auth_service.logout(token=input_token)

    mock_auth_repository.get_refresh_token_by_jti.assert_not_called()
    mock_verify_password.assert_not_called()
    mock_revoke_refresh_token.assert_not_called()


def test_logout_fails_when_refresh_token_not_found(
    mocker, auth_service, mock_auth_repository
):
    input_token = "dummy_token"

    mock_user_id = uuid.uuid4()
    mock_jti = uuid.uuid4()
    mock_decode_refresh_token = Mock(return_value=(mock_user_id, mock_jti))
    auth_service.decode_refresh_token = mock_decode_refresh_token

    mock_auth_repository.get_user_by_id.return_value = User(id=mock_user_id)
    mock_auth_repository.get_refresh_token_by_jti.return_value = None

    mock_verify_password = mocker.patch("app.services.auth.verify_password")

    mock_revoke_refresh_token = Mock()
    auth_service.revoke_refresh_token = mock_revoke_refresh_token

    with pytest.raises(CredentialException):
        auth_service.logout(token=input_token)

    mock_verify_password.assert_not_called()
    mock_revoke_refresh_token.assert_not_called()


def test_logout_fails_when_password_verification_fails(
    mocker, auth_service, mock_auth_repository
):
    input_token = "dummy_token"

    mock_user_id = uuid.uuid4()
    mock_jti = uuid.uuid4()
    mock_decode_refresh_token = Mock(return_value=(mock_user_id, mock_jti))
    auth_service.decode_refresh_token = mock_decode_refresh_token

    mock_auth_repository.get_user_by_id.return_value = User(id=mock_user_id)

    mock_refresh_token = RefreshToken(token="hashed_input_token", jti=mock_jti)
    mock_auth_repository.get_refresh_token_by_jti.return_value = mock_refresh_token

    mocker.patch("app.services.auth.verify_password", return_value=False)

    mock_revoke_refresh_token = Mock()
    auth_service.revoke_refresh_token = mock_revoke_refresh_token

    with pytest.raises(CredentialException):
        auth_service.logout(token=input_token)

    mock_revoke_refresh_token.assert_not_called()


def test_refresh_success(mocker, auth_service, mock_auth_repository):
    input_token = "dummy_token"

    mock_user_id = uuid.uuid4()
    mock_jti = uuid.uuid4()
    mock_decode_refresh_token = Mock(return_value=(mock_user_id, mock_jti))
    auth_service.decode_refresh_token = mock_decode_refresh_token

    mock_user = User(id=mock_user_id)
    mock_auth_repository.get_user_by_id.return_value = mock_user

    mock_refresh_token = RefreshToken(
        token="hashed_input_token", jti=mock_jti, revoked_at=None
    )
    mock_auth_repository.get_refresh_token_by_jti.return_value = mock_refresh_token

    mock_verify_password = mocker.patch(
        "app.services.auth.verify_password", return_value=True
    )

    mock_revoke_refresh_token = Mock()
    auth_service.revoke_refresh_token = mock_revoke_refresh_token

    mock_create_token = Mock(
        side_effect=[
            ("new_access_token", None, None),
            ("new_refresh_token", "dummy_expire", "dummy_jti"),
        ]
    )
    auth_service.create_token = mock_create_token

    mock_save_refresh_token = Mock()
    auth_service.save_refresh_token = mock_save_refresh_token

    token = auth_service.refresh(token=input_token)

    mock_decode_refresh_token.assert_called_once_with(token=input_token)
    mock_auth_repository.get_user_by_id.assert_called_once_with(mock_user_id)
    mock_auth_repository.get_refresh_token_by_jti.assert_called_once_with(jti=mock_jti)
    mock_verify_password.assert_called_once_with(input_token, mock_refresh_token.token)
    mock_revoke_refresh_token.assert_called_once_with(target=mock_refresh_token)
    assert mock_create_token.call_count == 2
    mock_create_token.assert_any_call(
        data={"sub": str(mock_user.id)}, token_kind="access"
    )
    mock_create_token.assert_any_call(
        data={"sub": str(mock_user.id)}, token_kind="refresh"
    )
    mock_save_refresh_token.assert_called_once_with(
        user_id=mock_user_id,
        token="new_refresh_token",
        expire="dummy_expire",
        jti="dummy_jti",
    )
    assert token.access_token == "new_access_token"
    assert token.refresh_token == "new_refresh_token"
    assert token.token_type == "bearer"


def test_refresh_fails_when_user_not_found(mocker, auth_service, mock_auth_repository):
    input_token = "dummy_token"

    mock_user_id = uuid.uuid4()
    mock_jti = uuid.uuid4()
    mock_decode_refresh_token = Mock(return_value=(mock_user_id, mock_jti))
    auth_service.decode_refresh_token = mock_decode_refresh_token

    mock_auth_repository.get_user_by_id.return_value = None

    mock_verify_password = mocker.patch("app.services.auth.verify_password")

    mock_revoke_refresh_token = Mock()
    auth_service.revoke_refresh_token = mock_revoke_refresh_token

    mock_create_token = Mock()
    auth_service.create_token = mock_create_token

    mock_save_refresh_token = Mock()
    auth_service.save_refresh_token = mock_save_refresh_token

    with pytest.raises(CredentialException):
        auth_service.refresh(token=input_token)

    mock_auth_repository.get_refresh_token_by_jti.assert_not_called()
    mock_verify_password.assert_not_called()
    mock_revoke_refresh_token.assert_not_called()
    mock_create_token.assert_not_called()
    mock_save_refresh_token.assert_not_called()


def test_refresh_fails_when_refresh_token_not_found(
    mocker, auth_service, mock_auth_repository
):
    input_token = "dummy_token"

    mock_user_id = uuid.uuid4()
    mock_jti = uuid.uuid4()
    mock_decode_refresh_token = Mock(return_value=(mock_user_id, mock_jti))
    auth_service.decode_refresh_token = mock_decode_refresh_token

    mock_user = User(id=mock_user_id)
    mock_auth_repository.get_user_by_id.return_value = mock_user

    mock_auth_repository.get_refresh_token_by_jti.return_value = None

    mock_verify_password = mocker.patch("app.services.auth.verify_password")

    mock_revoke_refresh_token = Mock()
    auth_service.revoke_refresh_token = mock_revoke_refresh_token

    mock_create_token = Mock()
    auth_service.create_token = mock_create_token

    mock_save_refresh_token = Mock()
    auth_service.save_refresh_token = mock_save_refresh_token

    with pytest.raises(CredentialException):
        auth_service.refresh(token=input_token)

    mock_verify_password.assert_not_called()
    mock_revoke_refresh_token.assert_not_called()
    mock_create_token.assert_not_called()
    mock_save_refresh_token.assert_not_called()


def test_refresh_fails_when_password_validation_fails(
    mocker, auth_service, mock_auth_repository
):
    input_token = "dummy_token"

    mock_user_id = uuid.uuid4()
    mock_jti = uuid.uuid4()
    mock_decode_refresh_token = Mock(return_value=(mock_user_id, mock_jti))
    auth_service.decode_refresh_token = mock_decode_refresh_token

    mock_user = User(id=mock_user_id)
    mock_auth_repository.get_user_by_id.return_value = mock_user

    mock_refresh_token = RefreshToken(
        token="hashed_input_token", jti=mock_jti, revoked_at=None
    )
    mock_auth_repository.get_refresh_token_by_jti.return_value = mock_refresh_token

    mocker.patch("app.services.auth.verify_password", return_value=False)

    mock_revoke_refresh_token = Mock()
    auth_service.revoke_refresh_token = mock_revoke_refresh_token

    mock_create_token = Mock()
    auth_service.create_token = mock_create_token

    mock_save_refresh_token = Mock()
    auth_service.save_refresh_token = mock_save_refresh_token

    with pytest.raises(CredentialException):
        auth_service.refresh(token=input_token)

    mock_revoke_refresh_token.assert_not_called()
    mock_create_token.assert_not_called()
    mock_save_refresh_token.assert_not_called()


def test_refresh_fails_when_target_has_already_been_revoked(
    mocker, auth_service, mock_auth_repository
):
    input_token = "dummy_token"

    mock_user_id = uuid.uuid4()
    mock_jti = uuid.uuid4()
    mock_decode_refresh_token = Mock(return_value=(mock_user_id, mock_jti))
    auth_service.decode_refresh_token = mock_decode_refresh_token

    mock_user = User(id=mock_user_id)
    mock_auth_repository.get_user_by_id.return_value = mock_user

    mock_refresh_token = RefreshToken(
        token="hashed_input_token", jti=mock_jti, revoked_at="dummy_revoked_at"
    )
    mock_auth_repository.get_refresh_token_by_jti.return_value = mock_refresh_token

    mocker.patch("app.services.auth.verify_password", return_value=True)

    mock_revoke_refresh_token = Mock()
    auth_service.revoke_refresh_token = mock_revoke_refresh_token

    mock_create_token = Mock()
    auth_service.create_token = mock_create_token

    mock_save_refresh_token = Mock()
    auth_service.save_refresh_token = mock_save_refresh_token

    with pytest.raises(TokenReuseException):
        auth_service.refresh(token=input_token)

    mock_revoke_refresh_token.assert_not_called()
    mock_create_token.assert_not_called()
    mock_save_refresh_token.assert_not_called()


def test_decode_refresh_token_success(auth_service):
    user_id = uuid.uuid4()
    jti = uuid.uuid4()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=10)

    to_encode = {
        "type": "refresh",
        "sub": str(user_id),
        "jti": str(jti),
        "exp": expire,
        "iat": now,
    }

    input_refresh_token = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    decoded_user_id, decoded_jti = auth_service.decode_refresh_token(
        input_refresh_token
    )

    assert decoded_user_id == user_id
    assert decoded_jti == jti


def test_decode_refresh_fails_token_when_jwt_decoding_fails(auth_service):
    input_refresh_token = "invalid.jwt.token"

    with pytest.raises(CredentialException):
        auth_service.decode_refresh_token(input_refresh_token)


def test_decode_refresh_fails_token_when_sub_cannot_be_converted_to_uuid(auth_service):
    invalid_sub = "invalid_sub"
    jti = uuid.uuid4()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=10)

    to_encode = {
        "type": "refresh",
        "sub": invalid_sub,
        "jti": str(jti),
        "exp": expire,
        "iat": now,
    }

    input_refresh_token = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    with pytest.raises(CredentialException):
        auth_service.decode_refresh_token(input_refresh_token)


def test_decode_refresh_fails_token_when_jti_cannot_be_converted_to_uuid(auth_service):
    user_id = uuid.uuid4()
    invalid_jti = "invalid_jti"
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=10)

    to_encode = {
        "type": "refresh",
        "sub": str(user_id),
        "jti": invalid_jti,
        "exp": expire,
        "iat": now,
    }

    input_refresh_token = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    with pytest.raises(CredentialException):
        auth_service.decode_refresh_token(input_refresh_token)


def test_decode_refresh_token_fails_when_type_in_payload_is_not_refresh(auth_service):
    user_id = uuid.uuid4()
    jti = uuid.uuid4()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=10)

    to_encode = {
        "type": "access",
        "sub": str(user_id),
        "jti": str(jti),
        "exp": expire,
        "iat": now,
    }

    input_refresh_token = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    with pytest.raises(CredentialException):
        auth_service.decode_refresh_token(input_refresh_token)


def test_decode_refresh_token_fails_when_sub_not_found_in_payload(auth_service):
    jti = uuid.uuid4()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=10)

    to_encode = {
        "type": "refresh",
        "jti": str(jti),
        "exp": expire,
        "iat": now,
    }

    input_refresh_token = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    with pytest.raises(CredentialException):
        auth_service.decode_refresh_token(input_refresh_token)


def test_decode_refresh_token_fails_when_jti_not_found_in_payload(auth_service):
    user_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=10)

    to_encode = {
        "type": "refresh",
        "sub": str(user_id),
        "exp": expire,
        "iat": now,
    }

    input_refresh_token = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    with pytest.raises(CredentialException):
        auth_service.decode_refresh_token(input_refresh_token)


def test_save_refresh_token(mocker, mock_auth_repository, auth_service):
    user_id = uuid.uuid4()
    token = "dummy_refresh_token"
    expire = datetime.now(timezone.utc) + timedelta(minutes=10)
    jti = uuid.uuid4()

    mock_get_password_hash = mocker.patch(
        "app.services.auth.get_password_hash", return_value="hashed_refresh_token"
    )

    auth_service.save_refresh_token(
        user_id=user_id, token=token, expire=expire, jti=jti
    )

    saved_refresh_token = mock_auth_repository.save_refresh_token.call_args.args[0]

    mock_get_password_hash.assert_called_with(token)
    mock_auth_repository.save_refresh_token.assert_called_once()
    assert saved_refresh_token.user_id == user_id
    assert saved_refresh_token.token == "hashed_refresh_token"
    assert saved_refresh_token.expires_at == expire
    assert saved_refresh_token.jti == jti
