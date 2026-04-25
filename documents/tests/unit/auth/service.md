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
