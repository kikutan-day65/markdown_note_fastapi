import uuid

from app.main import app


def test_read_me_returns_200(auth_client, user):
    url = app.url_path_for("read_me")
    result = auth_client.get(url)

    result_json = result.json()

    assert result.status_code == 200
    assert result_json["id"] == str(user.id)


def test_read_me_returns_401_when_credential_is_invalid(client):
    url = app.url_path_for("read_me")
    result = client.get(url)

    assert result.status_code == 401


def test_read_me_returns_403_when_user_is_inactive(inactive_client):
    url = app.url_path_for("read_me")
    result = inactive_client.get(url)

    assert result.status_code == 403


def test_create_user_returns_201(client, user_create_data):
    url = app.url_path_for("create_user")
    result = client.post(url, json=user_create_data.model_dump())

    result_json = result.json()

    assert result.status_code == 201
    assert result_json["username"] == user_create_data.username


def test_create_user_returns_409_when_user_already_exists(
    client, user_create_data, user
):
    url = app.url_path_for("create_user")
    result = client.post(url, json=user_create_data.model_dump())

    assert result.status_code == 409


def test_list_users_returns_200(auth_admin_client, users):
    url = app.url_path_for("list_users")
    result = auth_admin_client.get(url)

    result_json = result.json()

    assert result.status_code == 200
    assert len(result_json) == len(users)


def test_list_users_returns_401_when_credential_is_invalid(client, users):
    url = app.url_path_for("list_users")
    result = client.get(url)

    assert result.status_code == 401


def test_list_users_returns_403_when_user_is_not_admin(auth_client, users):
    url = app.url_path_for("list_users")
    result = auth_client.get(url)

    assert result.status_code == 403


def test_get_user_returns_200(auth_client, users):
    target_user_id = users[0].id
    url = app.url_path_for("get_user", id=target_user_id)
    result = auth_client.get(url)

    result_json = result.json()

    assert result.status_code == 200
    assert result_json["id"] == str(target_user_id)


def test_get_user_returns_404_when_user_not_found(auth_client):
    url = app.url_path_for("get_user", id=uuid.uuid4())
    result = auth_client.get(url)

    assert result.status_code == 404


def test_update_user_returns_200(auth_client, user):
    target_user_id = user.id
    url = app.url_path_for("update_user", id=target_user_id)

    update_data = {
        "username": "updated_username",
        "avatar_url": "updated_avatar_url",
    }

    result = auth_client.patch(url, json=update_data)

    result_json = result.json()

    assert result.status_code == 200
    assert result_json["id"] == str(target_user_id)
    assert result_json["username"] == update_data["username"]
    assert result_json["avatar_url"] == update_data["avatar_url"]


def test_update_user_returns_404_when_user_not_found(auth_admin_client):
    url = app.url_path_for("update_user", id=uuid.uuid4())
    update_data = {
        "username": "updated_username",
        "avatar_url": "updated_avatar_url",
    }
    result = auth_admin_client.patch(url, json=update_data)

    assert result.status_code == 404


def test_update_user_returns_403_when_user_is_not_admin_nor_owner(auth_client, users):
    target_user_id = users[0].id
    url = app.url_path_for("update_user", id=str(target_user_id))

    update_data = {
        "username": "updated_username",
        "avatar_url": "updated_avatar_url",
    }

    result = auth_client.patch(url, json=update_data)

    assert result.status_code == 403


def test_update_user_returns_409_when_user_already_exists(auth_admin_client, users):
    target_user_id = users[0].id
    existing_username = users[2].username

    url = app.url_path_for("update_user", id=str(target_user_id))

    update_data = {
        "username": existing_username,
    }

    result = auth_admin_client.patch(url, json=update_data)

    assert result.status_code == 409


def test_update_user_returns_401_when_credential_is_invalid(client, users):
    target_user_id = users[0].id
    url = app.url_path_for("update_user", id=str(target_user_id))

    update_data = {
        "username": "updated_username",
        "avatar_url": "updated_avatar_url",
    }

    result = client.patch(url, json=update_data)

    assert result.status_code == 401


def test_update_user_returns_403_when_user_is_inactive(inactive_client, users):
    target_user_id = users[0].id
    url = app.url_path_for("update_user", id=str(target_user_id))

    update_data = {
        "username": "updated_username",
        "avatar_url": "updated_avatar_url",
    }

    result = inactive_client.patch(url, json=update_data)

    assert result.status_code == 403


def test_delete_user_returns_204(auth_client, user, test_db_session):
    target_user_id = user.id
    url = app.url_path_for("delete_user", id=str(target_user_id))

    result = auth_client.delete(url)
    test_db_session.refresh(user)

    assert result.status_code == 204
    assert user.deleted_at is not None


def test_delete_user_returns_404_when_user_not_found(auth_admin_client):
    url = app.url_path_for("delete_user", id=uuid.uuid4())
    result = auth_admin_client.delete(url)

    assert result.status_code == 404


def test_delete_user_returns_403_when_user_is_not_admin_nor_owner(auth_client, users):
    target_user_id = users[0].id
    url = app.url_path_for("delete_user", id=str(target_user_id))

    result = auth_client.delete(url)

    assert result.status_code == 403


def test_delete_user_returns_401_when_credential_is_invalid(client, users):
    target_user_id = users[0].id
    url = app.url_path_for("delete_user", id=str(target_user_id))

    result = client.delete(url)

    assert result.status_code == 401


def test_delete_user_returns_403_when_user_is_inactive(inactive_client, users):
    target_user_id = users[0].id
    url = app.url_path_for("delete_user", id=str(target_user_id))

    result = inactive_client.delete(url)

    assert result.status_code == 403
