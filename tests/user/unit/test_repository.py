import uuid

import pytest


def test_save_success(user_repository, user):
    result = user_repository.save(user)

    assert result == user


def test_get_all_returns_user_list(user_repository, users):
    result = user_repository.get_all()

    assert len(result) == 2
    assert result[0] == users[0]
    assert result[1] == users[2]


def test_get_by_id_returns_user(user_repository, users):
    user_id = users[0].id

    result = user_repository.get_by_id(user_id)

    assert result == users[0]


def test_get_by_id_returns_none(user_repository, users):
    user_id = uuid.uuid4()

    result = user_repository.get_by_id(user_id)

    assert result is None


@pytest.mark.parametrize(
    "input_data",
    [
        {"username": "test_user_01", "email": None},
        {"username": None, "email": "test_user_01@example.com"},
    ],
)
def test_get_by_username_or_email_returns_user(user_repository, users, input_data):
    username = input_data["username"]
    email = input_data["email"]

    result = user_repository.get_by_username_or_email(username, email)

    assert result == users[0]


@pytest.mark.parametrize(
    "input_data",
    [
        {"username": "dummy_user", "email": None},
        {"username": None, "email": "dummy_user@example.com"},
    ],
)
def test_get_by_username_or_email_returns_none_when_user_not_found(
    user_repository, users, input_data
):
    username = input_data["username"]
    email = input_data["email"]

    result = user_repository.get_by_username_or_email(username, email)

    assert result is None


def test_get_by_username_returns_user(user_repository, users):
    username = users[0].username

    result = user_repository.get_by_username(username)

    assert result == users[0]


def test_get_by_username_returns_none(user_repository, users):
    username = "dummy_username"

    result = user_repository.get_by_username(username)

    assert result is None
