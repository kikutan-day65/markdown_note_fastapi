## POST `users/`

Create a new user.

**Input**

```json
{
    "username": "username",
    "email": "email@example.com",
    "password": "password"
}
```

**Output**

```json
{
    "id": "uuid",
    "username": "username",
    "email": "email@example.com",
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

## GET `users/`

List all users. Only for admin.

**Output**

```json
[
    {
        "id": "uuid",
        "username": "username",
        "email": "email@example.com",
        "is_admin": "bool",
        "is_active": "bool",
        "is_verified": "bool",
        "avatar_url": "xxx-xxx-xxx",
        "created_at": "YYYY-MM-DDTHH:MM:SSZ",
        "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
]
```

## GET `users/<id>/`

Get the specific user.

**Output**

```json
{
    "id": "uuid",
    "username": "username",
    "avatar_url": "xxx-xxx-xxx",
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

## PATCH `users/<id>/`

Patch the specific user. Only for admin.

**Input**

```json
{
    "username": "username",
    "avatar_url": "xxx-xxx-xxx"
}
```

**Output**

```json
{
    "id": "uuid",
    "username": "username",
    "avatar_url": "xxx-xxx-xxx",
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

## DELETE `users/<id>/`

Delete the specific user logically. Only for admin user.

## GET `users/me/`

Get the current user. Only for current user.

**Output**

```json
{
    "id": "uuid",
    "username": "username",
    "email": "email@example.com",
    "avatar_url": "xxx-xxx-xxx",
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

## PATCH `users/me/`

Patch current user. Only for current user.

**Input**

```json
{
    "username": "username",
    "avatar_url": "xxx-xxx-xxx"
}
```

**Output**

```json
{
    "id": "uuid",
    "username": "username",
    "avatar_url": "xxx-xxx-xxx",
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

## DELETE `users/me/`

Delete the current user logically. Only for current user.

## POST `users/me/change-email/`

Change current user's email address. Only for current user.

**Input**

```json
{
    "email": "new_email@example.com"
}
```

## POST `users/me/change-password/`

Change current user's password. Only for current user.

**Input**

```json
{
    "current_password": "current_password",
    "new_password": "new_password"
}
```
