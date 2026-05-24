import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

import jwt
import pytest

from app.core.settings import settings
from app.db.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.services.user import UserService


@pytest.fixture
def mock_user_repository():
    return Mock(spec=UserRepository)


@pytest.fixture
def user_service(mock_user_repository):
    return UserService(repository=mock_user_repository)


@pytest.fixture
def user_repository(test_db_session):
    return UserRepository(db=test_db_session)


@pytest.fixture
def user(test_db_session):
    user = User(
        id=uuid.uuid4(),
        username="test_user_00",
        email="test_user_00@example.com",
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
def inactive_user(test_db_session):
    user = User(
        id=uuid.uuid4(),
        username="test_user_00",
        email="test_user_00@example.com",
        password_hash="hashed_password",
        is_verified=True,
        is_active=False,
    )

    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)

    return user


@pytest.fixture
def user_create_data():
    return UserCreate(
        username="test_user_00",
        email="test_user_00@example.com",
        password="password123",
        avatar_url="avatar-url",
    )


@pytest.fixture
def users(test_db_session):
    users = []

    for i in range(1, 4):
        deleted_time = None
        if i == 2:
            deleted_time = datetime.now(timezone.utc)

        num = str(i).zfill(2)

        users.append(
            User(
                id=uuid.uuid4(),
                username=f"test_user_{num}",
                email=f"test_user_{num}@example.com",
                password_hash="hashed_password",
                is_verified=True,
                deleted_at=deleted_time,
            )
        )

    test_db_session.add_all(users)
    test_db_session.commit()

    for user in users:
        test_db_session.refresh(user)

    return users


def create_access_token_for_test(user_id: uuid.UUID) -> str:
    to_encode = {"sub": str(user_id)}
    now = datetime.now(timezone.utc)

    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = now + expires_delta

    to_encode.update(
        {
            "type": "access",  # access/refresh
            "exp": expire,  # token expiration time
            "iat": now,  # token issued time
        }
    )

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@pytest.fixture
def auth_client(client, user):
    # Create access token
    user_id = user.id
    encoded_jwt = create_access_token_for_test(user_id)

    # Set access token in client headers
    client.headers.update({"Authorization": f"Bearer {encoded_jwt}"})

    return client


@pytest.fixture
def inactive_client(client, inactive_user):
    # Create access token
    user_id = inactive_user.id
    encoded_jwt = create_access_token_for_test(user_id)

    # Set access token in client headers
    client.headers.update({"Authorization": f"Bearer {encoded_jwt}"})

    return client


@pytest.fixture
def auth_admin_client(client, admin_user):
    # Create access token
    user_id = admin_user.id
    encoded_jwt = create_access_token_for_test(user_id)

    # Set access token in client headers
    client.headers.update({"Authorization": f"Bearer {encoded_jwt}"})

    return client
