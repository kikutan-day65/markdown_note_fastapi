import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.article import Article
    from app.db.models.tag import Tag


class ArticleTag(Base):
    __tablename__ = "article_tags"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Foreign keys
    tag_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tags.id"), nullable=False
    )
    article_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("articles.id"), nullable=False
    )

    # Relationships (ORM)
    tag: Mapped["Tag"] = relationship("Tag", back_populates="article_tags")
    article: Mapped["Article"] = relationship("Article", back_populates="article_tags")
