from app.db.models.user import User


def test_create_user_success(
    mocker, mock_user_repository, user_service, user_create_data
):
    new_user = User()

    mock_get_password_hash = mocker.patch(
        "app.services.user.get_password_hash", return_value="hashed_password"
    )
    mock_user_repository.save.return_value = new_user

    result = user_service.create_user(user_create_data)

    mock_get_password_hash.assert_called_once_with(user_create_data.password)
    mock_user_repository.save.assert_called_once()

    saved_new_user = mock_user_repository.save.call_args.args[0]

    assert saved_new_user.username == user_create_data.username
    assert saved_new_user.email == user_create_data.email
    assert saved_new_user.password_hash == mock_get_password_hash.return_value
    assert saved_new_user.avatar_url == user_create_data.avatar_url
    assert result == new_user


def test_list_users_success(mock_user_repository, user_service):
    users = [User(), User()]

    mock_user_repository.get_all.return_value = users

    result = user_service.list_users()

    mock_user_repository.get_all.assert_called_once()
    assert result == users
