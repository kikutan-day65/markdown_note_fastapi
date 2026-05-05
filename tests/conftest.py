import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock

# Ensure tests are running with .test.env
TARGET_ENV_FILE = os.getenv("ENV_FILE")

if TARGET_ENV_FILE != ".env.test":
    raise RuntimeError(
        f"Tests must run with ENV_FILE=.env.test, but got {TARGET_ENV_FILE!r}"
    )

# Ensure .env.test exists
if not Path(TARGET_ENV_FILE).exists():
    raise RuntimeError(f"Test env file does not exist: {TARGET_ENV_FILE}")

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings
from app.db.base import Base
from app.db.models.refresh_token import RefreshToken
from app.db.models.user import User
from app.repositories.auth import AuthRepository
from app.services.auth import AuthService

# Ensure DATABASE_URL points to a test db
url = make_url(settings.DATABASE_URL)
if url.database is None or "test" not in url.database:
    raise RuntimeError(
        f"Refusing to run tests against non-test database: {url.database!r}"
    )

# Prepare test db
test_engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionTestLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)


@pytest.fixture
def setup_test_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def test_db_session(setup_test_db):
    db = SessionTestLocal()

    try:
        yield db
    finally:
        db.close()


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
def mock_auth_repository():
    return Mock(spec=AuthRepository)


@pytest.fixture
def auth_service(mock_auth_repository):
    return AuthService(repository=mock_auth_repository)


@pytest.fixture
def auth_repository(test_db_session):
    return AuthRepository(db=test_db_session)


class DummyFormData:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


@pytest.fixture
def dummy_form_data():
    return DummyFormData(username="testuser", password="password123")
