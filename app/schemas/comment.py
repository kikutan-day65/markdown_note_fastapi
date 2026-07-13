import uuid
from datetime import datetime

from app.schemas.article import ArticleBriefSummary
from app.schemas.base import ORMBase
from app.schemas.user import UserSummary


# ===== REQUEST =====
class CommentCreate(ORMBase):
    body: str


class CommentUpdate(ORMBase):
    body: str


# ===== RESPONSE =====
class CommentPublic(ORMBase):
    id: uuid.UUID
    body: str
    created_at: datetime
    updated_at: datetime
    user: UserSummary
    article: ArticleBriefSummary


class CommentSummaryWithUser(ORMBase):
    id: uuid.UUID
    body: str
    created_at: datetime
    updated_at: datetime
    user: UserSummary


class CommentSummaryWithArticle(ORMBase):
    id: uuid.UUID
    body: str
    created_at: datetime
    updated_at: datetime
    article: ArticleBriefSummary
