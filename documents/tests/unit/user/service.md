## create_user

- [x] Calls `get_password_hash()` with input password
- [x] Calls `repository.save()` with correct argument
  - [x] Sets `username` from input user data
  - [x] Sets `email` from input user data
  - [x] Sets `password_hash` from hashed input password
  - [x] Sets `avatar_url` from input user data
- [x] Returns result of `repository.save()`

## list_users

- [x] Calls `repository.get_all()`
- [x] Returns result of `repository.get_all()`
