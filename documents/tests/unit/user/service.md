## create_user

- [x] Calls `get_password_hash()` with input password
- [x] Calls `repository.save()` with correct argument
  - [x] Sets `username` from input user data
  - [x] Sets `email` from input user data
  - [x] Sets `password_hash` from hashed input password
  - [x] Sets `avatar_url` from input user data
- [x] Returns result of `repository.save()`
- [x] Raises `UserAlreadyExistsException` when user already exists

## list_users

- [x] Calls `repository.get_all()`
- [x] Returns result of `repository.get_all()`

## retrieve_user

- [x] Calls `repository.get_by_id()` with correct argument
- [x] Returns result of `repository.get_by_id()`
- [x] Raises `UserNotFoundException` when user not found

## update_user

### Request by admin user

- [x] Calls `repository.get_by_id()` with input user id
- [x] Calls `repository.get_by_username()` when update data includes `username`
- [x] Calls `repository.save()` with correct target user
- [x] Returns result of `repository.save()`

### Request by owner

- [x] Calls `repository.get_by_id()` with input user id
- [x] Calls `repository.get_by_username()` when update data includes `username`
- [x] Calls `repository.save()` with correct target user
- [x] Returns result of `repository.save()`

### Negative cases

- [x] Raises `UserNotFoundException` when user not found
- [x] Raises `PermissionDeniedException` when request user is not admin and not owner
- [x] Raises `UserAlreadyExistsException` when update data includes existing `username`
