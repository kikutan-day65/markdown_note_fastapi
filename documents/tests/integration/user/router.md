# read_me

- [x] Returns 200
- [x] Returns 401 when credential is invalid
- [x] Returns 403 when user is inactive

# create_user

- [x] Returns 201
- [x] Returns 409 when user is already exists

# list_users

- [x] Returns 200
- [x] Returns 401 when credential is invalid
- [x] Returns 403 when user is not admin

# get_user

- [x] Returns 200
- [x] Returns 404 when user not found

# update_user

- [x] Returns 200
- [x] Returns 404 when user not found
- [x] Returns 403 when user is not admin nor owner
- [x] Returns 409 when user already exists
- [x] Returns 401 when credential is invalid
- [x] Returns 403 when user is inactive

# delete_user

- [x] Returns 204
- [x] Returns 404 when user not found
- [x] Returns 403 when user is not admin nor owner
- [x] Returns 401 when credential is invalid
- [x] Returns 403 when user is inactive
