import uuid

import pytest

from app.core.exceptions import (
    PermissionDeniedException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.models.user import User
from app.schemas.user import UserUpdate


def test_create_user_success(
    mocker, mock_user_repository, user_service, user_create_data
):
    new_user = User()

    mock_get_password_hash = mocker.patch(
        "app.services.user.get_password_hash", return_value="hashed_password"
    )
    mock_user_repository.get_by_username_or_email.return_value = None
    mock_user_repository.save.return_value = new_user

    result = user_service.create_user(user_create_data)

    mock_user_repository.get_by_username_or_email.assert_called_once_with(
        username=user_create_data.username, email=user_create_data.email
    )
    mock_get_password_hash.assert_called_once_with(user_create_data.password)
    mock_user_repository.save.assert_called_once()

    saved_new_user = mock_user_repository.save.call_args.args[0]

    assert saved_new_user.username == user_create_data.username
    assert saved_new_user.email == user_create_data.email
    assert saved_new_user.password_hash == mock_get_password_hash.return_value
    assert saved_new_user.avatar_url == user_create_data.avatar_url
    assert result == new_user


def test_create_user_fails_when_user_already_exists(
    mocker, mock_user_repository, user_service, user_create_data
):
    new_user = User()

    mock_user_repository.get_by_username_or_email.return_value = new_user
    mock_get_password_hash = mocker.patch("app.services.user.get_password_hash")

    with pytest.raises(UserAlreadyExistsException):
        user_service.create_user(user_create_data)

    mock_user_repository.get_by_username_or_email.assert_called_once_with(
        username=user_create_data.username, email=user_create_data.email
    )
    mock_get_password_hash.assert_not_called()
    mock_user_repository.save.assert_not_called()


def test_list_users_success(mock_user_repository, user_service):
    users = [User(), User()]

    mock_user_repository.get_all.return_value = users

    result = user_service.list_users()

    mock_user_repository.get_all.assert_called_once()
    assert result == users


def test_retrieve_user_success(mock_user_repository, user_service):
    user_id = uuid.uuid4()
    user = User(id=user_id)

    mock_user_repository.get_by_id.return_value = user

    result = user_service.retrieve_user(user_id)

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    assert result == user


def test_retrieve_user_fails_when_user_not_found(mock_user_repository, user_service):
    user_id = uuid.uuid4()

    mock_user_repository.get_by_id.return_value = None

    with pytest.raises(UserNotFoundException):
        user_service.retrieve_user(user_id)


def test_update_user_success_by_admin_user(
    mock_user_repository, user_service, user, admin_user
):
    user_id = user.id
    user_data = UserUpdate(username="updated_username")

    mock_user_repository.get_by_id.return_value = user
    mock_user_repository.get_by_username.return_value = None
    mock_user_repository.save.return_value = user

    result = user_service.update_user(user_id, user_data, admin_user)

    mock_user_repository.save.assert_called_once()

    saved_user = mock_user_repository.save.call_args.args[0]

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.get_by_username.assert_called_once_with(
        username=user_data.username
    )
    assert saved_user.username == user_data.username
    assert result.username == user_data.username


def test_update_user_success_by_owner(mock_user_repository, user_service, user):
    user_id = user.id
    user_data = UserUpdate(avatar_url="updated-avatar-url")

    mock_user_repository.get_by_id.return_value = user
    mock_user_repository.get_by_username.return_value = None
    mock_user_repository.save.return_value = user

    result = user_service.update_user(user_id, user_data, user)

    mock_user_repository.save.assert_called_once()

    saved_user = mock_user_repository.save.call_args.args[0]

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.get_by_username.assert_not_called()
    assert saved_user.avatar_url == user_data.avatar_url
    assert result.avatar_url == user_data.avatar_url


def test_update_user_fails_when_user_not_found(
    mock_user_repository, user_service, user, admin_user
):
    user_id = user.id
    user_data = UserUpdate(username="updated_username")

    mock_user_repository.get_by_id.return_value = None

    with pytest.raises(UserNotFoundException):
        user_service.update_user(user_id, user_data, admin_user)

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.get_by_username.assert_not_called()
    mock_user_repository.save.assert_not_called()


def test_update_user_fails_when_not_admin_and_not_owner(
    mock_user_repository, user_service, user
):
    user_id = uuid.uuid4()
    user_data = UserUpdate(username="updated_username")

    mock_user_repository.get_by_id.return_value = User(id=uuid.uuid4())

    with pytest.raises(PermissionDeniedException):
        user_service.update_user(user_id, user_data, user)

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.get_by_username.assert_not_called()
    mock_user_repository.save.assert_not_called()


def test_update_user_fails_when_username_is_already_taken(
    mock_user_repository, user_service, user
):
    user_id = user.id
    user_data = UserUpdate(username="updated_username")
    existing_user = User(id=uuid.uuid4(), username="updated_username")

    mock_user_repository.get_by_id.return_value = user
    mock_user_repository.get_by_username.return_value = existing_user

    with pytest.raises(UserAlreadyExistsException):
        user_service.update_user(user_id, user_data, user)

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.get_by_username.assert_called_once_with(
        username=user_data.username
    )
    mock_user_repository.save.assert_not_called()


def test_delete_user_success_by_admin_user(
    mock_user_repository, user_service, user, admin_user
):
    user_id = user.id

    mock_user_repository.get_by_id.return_value = user

    user_service.delete_user(user_id, admin_user)

    mock_user_repository.save.assert_called_once_with(user)

    deleted_user = mock_user_repository.save.call_args.args[0]

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    assert deleted_user.deleted_at is not None


def test_delete_user_success_by_owner(mock_user_repository, user_service, user):
    user_id = user.id

    mock_user_repository.get_by_id.return_value = user

    user_service.delete_user(user_id, user)

    mock_user_repository.save.assert_called_once_with(user)

    deleted_user = mock_user_repository.save.call_args.args[0]

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    assert deleted_user.deleted_at is not None


def test_test_delete_user_fails_when_user_not_found(
    mock_user_repository, user_service, user
):
    user_id = uuid.uuid4()

    mock_user_repository.get_by_id.return_value = None

    with pytest.raises(UserNotFoundException):
        user_service.delete_user(user_id, user)

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.save.assert_not_called()


def test_delete_user_fails_when_not_admin_and_not_owner(
    mock_user_repository, user_service, user
):
    user_id = uuid.uuid4()
    target = User(id=uuid.uuid4())

    mock_user_repository.get_by_id.return_value = target

    with pytest.raises(PermissionDeniedException):
        user_service.delete_user(user_id, user)

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.save.assert_not_called()
