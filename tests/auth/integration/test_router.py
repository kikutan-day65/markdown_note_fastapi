from app.main import app


def test_login_returns_200_when_login_succeeds_with_username(
    client, integration_test_user, username_login_form_data
):
    url = app.url_path_for("login")
    result = client.post(url, data=username_login_form_data)

    assert result.status_code == 200


def test_login_returns_200_when_login_succeeds_with_email(
    client, integration_test_user, email_login_form_data
):
    url = app.url_path_for("login")
    result = client.post(url, data=email_login_form_data)

    assert result.status_code == 200


def test_login_returns_401_when_credential_is_invalid(
    client, integration_test_user, username_login_form_data
):
    data = username_login_form_data
    data["password"] = "invalid_password"

    url = app.url_path_for("login")
    result = client.post(url, data=data)

    assert result.status_code == 401


def test_refresh_returns_200_when_refresh_succeeds(
    client, integration_test_refresh_token
):
    token = {"refresh_token": integration_test_refresh_token}

    url = app.url_path_for("refresh")
    result = client.post(url, json=token)

    assert result.status_code == 200


def test_refresh_returns_401_when_refresh_fails(client, integration_test_refresh_token):
    token = {"refresh_token": "invalid_refresh_token"}

    url = app.url_path_for("refresh")
    result = client.post(url, json=token)

    assert result.status_code == 401
