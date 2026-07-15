## GET `/comments/{comment_id}`

Retrieve the specific comment

**Response**

```json
{
  "id": "uuid",
  "body": "comment body",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "user": {
    "id": "uuid",
    "username": "username"
  },
  "article": {
    "id": "uuid",
    "title": "title"
  }
}
```

## PATCH `/comments/{comment_id}`

Update the specific comment

**Request**

```json
{
  "body": "comment body"
}
```

**Response**

```json
{
  "id": "uuid",
  "body": "comment body",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "user": {
    "id": "uuid",
    "username": "username"
  },
  "article": {
    "id": "uuid",
    "title": "title"
  }
}
```

## DELETE `/comments/{comment_id}`

Delete the specific comment logically
