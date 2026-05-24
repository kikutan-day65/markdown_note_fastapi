import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

import jwt
import pytest

from app.core.security import get_password_hash
from app.core.settings import settings
from app.db.models.refresh_token import RefreshToken
from app.db.models.user import User
from app.repositories.auth import AuthRepository
from app.services.auth import AuthService


class DummyFormData:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


@pytest.fixture
def mock_auth_repository():
    return Mock(spec=AuthRepository)


@pytest.fixture
def auth_service(mock_auth_repository):
    return AuthService(repository=mock_auth_repository)


@pytest.fixture
def auth_repository(test_db_session):
    return AuthRepository(db=test_db_session)


@pytest.fixture
def dummy_form_data():
    return DummyFormData(username="testuser", password="password123")


@pytest.fixture
def username_login_form_data():
    return {
        "username": "integration_test_user",
        "password": "password123",
    }


@pytest.fixture
def email_login_form_data():
    return {
        "username": "integration_test_user@example.com",
        "password": "password123",
    }


@pytest.fixture
def user(test_db_session):
    user = User(
        id=uuid.uuid4(),
        username="test_user_01",
        email="test_user_01@example.com",
        password_hash="hashed_password",
        is_verified=True,
    )

    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)

    return user


@pytest.fixture
def admin_user(test_db_session):
    user = User(
        id=uuid.uuid4(),
        username="admin_user",
        email="admin_user@example.com",
        password_hash="hashed_password",
        is_verified=True,
        is_admin=True,
        is_active=True,
    )

    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)

    return user


@pytest.fixture
def deleted_user(test_db_session):
    user = User(
        id=uuid.uuid4(),
        username="deleted_user",
        email="test_user_01@example.com",
        password_hash="hashed_password",
        deleted_at=datetime.now(timezone.utc),
    )

    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)

    return user


@pytest.fixture
def refresh_token(user):
    refresh_token = RefreshToken(
        jti=uuid.uuid4(),
        token="hashed_refresh_token",
        expires_at=datetime.now(timezone.utc),
        user_id=user.id,
    )

    return refresh_token


@pytest.fixture
def saved_refresh_token(test_db_session, user):
    refresh_token = RefreshToken(
        id=uuid.uuid4(),
        jti=uuid.uuid4(),
        token="hashed_refresh_token",
        expires_at=datetime.now(timezone.utc),
        user_id=user.id,
    )

    test_db_session.add(refresh_token)
    test_db_session.commit()
    test_db_session.refresh(refresh_token)

    return refresh_token


@pytest.fixture
def integration_test_user(test_db_session):
    plain_password = "password123"

    user = User(
        id=uuid.uuid4(),
        username="integration_test_user",
        email="integration_test_user@example.com",
        password_hash=get_password_hash(plain_password),
        is_verified=True,
    )

    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)

    return user


@pytest.fixture
def integration_test_refresh_token(test_db_session, integration_test_user):
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    jti = uuid.uuid4()

    to_encode = {
        "sub": str(integration_test_user.id),
        "type": "refresh",
        "exp": expire,
        "iat": now,
        "jti": str(jti),
    }

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    refresh_token = RefreshToken(
        id=uuid.uuid4(),
        jti=jti,
        token=get_password_hash(encoded_jwt),
        expires_at=expire,
        user_id=integration_test_user.id,
    )

    test_db_session.add(refresh_token)
    test_db_session.commit()
    test_db_session.refresh(refresh_token)

    return encoded_jwt
