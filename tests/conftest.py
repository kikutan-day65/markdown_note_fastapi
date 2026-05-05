import os
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
