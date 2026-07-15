import uuid
from datetime import datetime

from pydantic import Field

from app.schemas.base import ORMBase
from app.schemas.tag import TagSummary
from app.schemas.user import UserSummary


# ===== REQUEST =====
class ArticleCreate(ORMBase):
    title: str
    content: str
    tag_ids: list[uuid.UUID] = Field(default_factory=list)


class ArticleUpdate(ORMBase):
    title: str | None
    content: str | None
    tag_ids: list[uuid.UUID] | None = None


# ===== RESPONSE =====
class ArticleBriefSummary(ORMBase):
    id: uuid.UUID
    title: str


class ArticleSummaryWithUser(ORMBase):
    id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    user: UserSummary
    tags: list[TagSummary]
    likes_count: int = 0


class ArticleSummaryWithoutUser(ORMBase):
    id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    tags: list[TagSummary]
    likes_count: int = 0


class ArticlePublic(ORMBase):
    id: uuid.UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user: UserSummary
    tags: list[TagSummary]
    likes_count: int = 0
