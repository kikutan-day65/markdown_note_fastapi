## POST `/users`

Create a new user

**Request**

```json
{
  "username": "username",
  "email": "email@example.com",
  "password": "password",
  "avatar_url": "xxx-xxx-xxx"
}
```

**Response**

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

## ❌ GET `/users`

List all users

**Response**

```json
{
  "items": [
    {
      "id": "uuid",
      "username": "username",
      "avatar_url": "xxx-xxx-xxx",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ",
      "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 10,
  "total_pages": 10,
  "has_next": true,
  "has_previous": false
}
```

## GET `/users/{user_id}`

Get the specific user

**Response**

```json
{
  "id": "uuid",
  "username": "username",
  "avatar_url": "xxx-xxx-xxx",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

## GET `/users/{user_id}/articles`

Get the specific user's articles

```json
{
  "items": [
    {
      "id": "uuid",
      "title": "title",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ",
      "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
      "tags": [
        { "id": "uuid", "name": "tag01" },
        { "id": "uuid", "name": "tag02" },
        { "id": "uuid", "name": "tag03" }
      ],
      "likes_count": 100
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 10,
  "total_pages": 10,
  "has_next": true,
  "has_previous": false
}
```

## GET `/users/me`

Get the current user

**Response**

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

## PATCH `/users/me`

Patch current user

**Request**

```json
{
  "username": "username",
  "avatar_url": "xxx-xxx-xxx"
}
```

**Response**

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

## DELETE `/users/me`

Delete the current user logically

## GET `/users/me/articles`

Get the current user's articles.

```json
{
  "items": [
    {
      "id": "uuid",
      "title": "title",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ",
      "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
      "tags": [
        { "id": "uuid", "name": "tag01" },
        { "id": "uuid", "name": "tag02" },
        { "id": "uuid", "name": "tag03" }
      ],
      "likes_count": 100
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 10,
  "total_pages": 10,
  "has_next": true,
  "has_previous": false
}
```

## GET `/users/me/comments`

List all the user's posted comments with pagination

**Response**

```json
{
  "items": [
    {
      "id": "uuid",
      "body": "comment body",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ",
      "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
      "article": {
        "id": "uuid",
        "title": "title"
      }
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 10,
  "total_pages": 10,
  "has_next": true,
  "has_previous": false
}
```
