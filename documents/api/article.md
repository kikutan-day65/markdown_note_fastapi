## POST `/articles`

Create a new article

**Request**

```json
{
  "title": "title",
  "content": "content",
  "tag_ids": ["uuid", "uuid", "uuid"]
}
```

**Response**

```json
{
  "id": "uuid",
  "title": "title",
  "content": "content",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "user": {
    "id": "uuid",
    "username": "username"
  },
  "tags": [
    { "id": "uuid", "name": "tag01" },
    { "id": "uuid", "name": "tag02" },
    { "id": "uuid", "name": "tag03" }
  ],
  "likes_count": 0
}
```

## GET `/articles`

List all articles with pagination

**Response**

```json
{
  "items": [
    {
      "id": "uuid",
      "title": "title",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ",
      "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
      "user": {
        "id": "uuid",
        "username": "username"
      },
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

## GET `/articles/{article_id}`

Get the specific article

**Response**

```json
{
  "id": "uuid",
  "title": "title",
  "content": "content",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "user": {
    "id": "uuid",
    "username": "username"
  },
  "tags": [
    { "id": "uuid", "name": "tag01" },
    { "id": "uuid", "name": "tag02" },
    { "id": "uuid", "name": "tag03" }
  ],
  "likes_count": 100
}
```

## PATCH `/articles/{article_id}`

Update the specific article

**Request**

```json
{
  "title": "title",
  "content": "content",
  "tag_ids": ["uuid", "uuid", "uuid"]
}
```

**Response**

```json
{
  "id": "uuid",
  "title": "title",
  "content": "content",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "user": {
    "id": "uuid",
    "username": "username"
  },
  "tags": [
    { "id": "uuid", "name": "tag01" },
    { "id": "uuid", "name": "tag02" },
    { "id": "uuid", "name": "tag03" }
  ],
  "likes_count": 100
}
```

## DELETE `/articles/{article_id}`

Delete the specific article logically

## POST `/articles/{article_id}/like`

Like the specific article

## DELETE `/articles/{article_id}/unlike`

Unlike the specific article

## POST `/articles/{article_id}/comments`

Create a new comment to the specific article

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

## GET `/articles/{article_id}/comments`

List all article's comments with pagination

**Response**

```json
{
  "items": [
    {
      "id": "uuid",
      "body": "comment body",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ",
      "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
      "user": {
        "id": "uuid",
        "username": "username"
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
