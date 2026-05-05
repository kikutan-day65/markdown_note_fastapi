import pytest


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
