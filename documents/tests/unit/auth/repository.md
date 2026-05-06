## get_user_by_identifier

- [x] Returns specific User object when `username` is used for identifier
- [x] Returns specific User object when `email` is used for identifier
- [x] Returns `None` when user not found
- [x] Returns `None` when user found but already deleted

## get_user_by_id

- [x] Returns specific User object
- [x] Returns `None` when user not found
- [x] Returns `None` when user found but already deleted

## save_refresh_token

- [x] Saves `RefreshToken`
  - [x] `jti` matches `jti` in input `RefreshToken`
  - [x] `token` in `RefreshToken` matches token in input `RefreshToken`
  - [x] `user_id` in `RefreshToken` matches user_id in input `RefreshToken`

## get_refresh_token_by_jti

- [x] Returns specific `RefreshToken`
- [x] Returns `None` when refresh token not found
