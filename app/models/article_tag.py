from sqlalchemy import Column, ForeignKey, Table, Uuid

from app.db.base import Base

article_tags = Table(
    "article_tags",
    Base.metadata,
    Column(
        "article_id",
        Uuid(as_uuid=True),
        ForeignKey("articles.id"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        Uuid(as_uuid=True),
        ForeignKey("tags.id"),
        primary_key=True,
    ),
)
