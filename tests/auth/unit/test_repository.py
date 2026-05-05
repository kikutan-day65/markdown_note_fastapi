import uuid

import pytest
from sqlalchemy import select

from app.db.models.refresh_token import RefreshToken


@pytest.mark.parametrize("identifier_field", ["username", "email"])
def test_get_user_by_identifier_success(auth_repository, user, identifier_field):
    identifier = getattr(user, identifier_field)

    result = auth_repository.get_user_by_identifier(identifier)

    assert result is not None
    assert result.id == user.id


def test_get_user_by_identifier_returns_none_when_user_not_found(auth_repository, user):
    identifier = "invalid_identifier"

    result = auth_repository.get_user_by_identifier(identifier)

    assert result is None


def test_get_user_by_identifier_returns_none_when_user_found_but_already_deleted(
    auth_repository, deleted_user
):
    identifier = deleted_user.username

    result = auth_repository.get_user_by_identifier(identifier)

    assert result is None


def test_get_user_by_id_success(auth_repository, user):
    user_id = user.id

    result = auth_repository.get_user_by_id(user_id)

    assert result is not None
    assert result.id == user_id


def test_get_user_by_id_returns_none_when_user_not_found(auth_repository, user):
    user_id = uuid.uuid4()

    result = auth_repository.get_user_by_id(user_id)

    assert result is None


def test_get_user_by_id_returns_none_when_user_found_but_already_deleted(
    auth_repository, deleted_user
):
    user_id = deleted_user.id

    result = auth_repository.get_user_by_id(user_id)

    assert result is None


def test_save_refresh_token_success(auth_repository, refresh_token, test_db_session):
    auth_repository.save_refresh_token(refresh_token)

    saved = test_db_session.scalar(select(RefreshToken))

    assert saved.jti == refresh_token.jti
    assert saved.user_id == refresh_token.user_id
    assert saved.token == refresh_token.token
