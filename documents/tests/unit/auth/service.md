## authenticate_user

- [x] Returns `User` object
- [x] Returns `None` when identifier is empty
- [x] Returns `None` when password is empty
- [x] Returns `None` when user cannot be retrieved by identifier
- [x] Returns `None` when password verification fails
- [x] `verify_password()` is called to avoid timing-attack when user cannot be retrieved by identifier

## create_token

- [x] Returns valid encoded JWT token for access token
  - [x] Sets `"access"` in `"type"` for access token
  - [x] `"exp"` is greater than current time for access token
  - [x] `"iat"` is within ±5 seconds of current time for access token
  - [x] `"jti'` is not set for access token
- [x] Returns `expire` that is greater than current time for access token
- [x] Returns `None` in `jti` for access token

- [x] Returns valid encoded JWT token for refresh token
  - [x] Sets `"refresh"` in `"type"` for refresh token
  - [x] `"exp"` is greater than current time for refresh token
  - [x] `"iat"` is within ±5 seconds of current time for refresh token
  - [x] `"jti"` is set for refresh token
- [x] Returns `expire` that is greater than current time for refresh token
- [x] Returns valid UUID in `jti` for refresh token

- [x] Returns `expire` when `expires_delta` is passed as argument
- [x] Raise `ValueError` when token kind is invalid

## login

- [x] Calls `authenticate_user()` with correct identifier and password
- [x] Calls `create_token()` twice
  - [x] Once with token kind `access`
  - [x] Once with token kind `refresh`
- [x] Calls `save_refresh_token()` with correct arguments
- [x] Returns valid `Token`
  - [x] access token in `Token` matches the returned value of `access_token`
  - [x] refresh token in `Token` matches the returned value of `refresh_token`
  - [x] type in `Token` matches `bearer`
- [x] Raise `AuthenticationException`
  - [x] `create_token()` is not called
  - [x] `save_refresh_token()` is not called

## logout

- [x] Calls `decode_refresh_token()`
- [x] Calls `get_user_by_id()`
- [x] Calls `get_refresh_token_by_jti()`
- [x] Calls `verify_password()`
- [x] Calls `revoke_refresh_token()`
- [x] Raises `CredentialException` when User object is not retrieved
  - [x] `get_refresh_token_by_jti()` is not called
  - [x] `verify_password()` is not called
  - [x] `revoke_refresh_token()` is not called
- [x] Raises `CredentialException` when RefreshToken object is not retrieved
  - [x] `verify_password()` is not called
  - [x] `revoke_refresh_token()` is not called
- [x] Raises `CredentialException` when password validation fails
  - [x] `revoke_refresh_token()` is not called

## refresh

- [x] Calls `decode_refresh_token()`
- [x] Calls `get_user_by_id()`
- [x] Calls `get_refresh_token_by_jti()`
- [x] Calls `verify_password()`
- [x] Calls `revoke_refresh_token()`
- [x] Calls `create_token()` twice
  - [x] Once with token kind `access`
  - [x] Once with token kind `refresh`
- [x] Calls `save_refresh_token()` with correct arguments
- [x] Returns valid `Token`
  - [x] access token in `Token` matches the returned value of `new_access_token`
  - [x] refresh token in `Token` matches the returned value of `new_refresh_token`
  - [x] type in `Token` matches `bearer`
- [x] Raises `CredentialException` when User object is not retrieved
  - [x] `get_refresh_token_by_jti()` is not called
  - [x] `verify_password()` is not called
  - [x] `revoke_refresh_token()` is not called
  - [x] `create_token()` is not called
  - [x] `save_refresh_token()` is not called
- [x] Raises `CredentialException` when RefreshToken object is not retrieved
  - [x] `verify_password()` is not called
  - [x] `revoke_refresh_token()` iw not called
  - [x] `create_token()` is not called
  - [x] `save_refresh_token()` is not called
- [x] Raises `CredentialException` when password validation fails
  - [x] `revoke_refresh_token()` iw not called
  - [x] `create_token()` is not called
  - [x] `save_refresh_token()` is not called
- [x] Raises `TokenReuseException` when the target RefreshToken has already been revoked
  - [x] `revoke_refresh_token()` iw not called
  - [x] `create_token()` is not called
  - [x] `save_refresh_token()` is not called
