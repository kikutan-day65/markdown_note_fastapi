import os
from pathlib import Path

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
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.core.settings import settings
from app.db.base import Base
from app.main import app

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
def override_get_db(setup_test_db):
    def _get_test_db():
        db = SessionTestLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_test_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client(override_get_db):
    return TestClient(app)
