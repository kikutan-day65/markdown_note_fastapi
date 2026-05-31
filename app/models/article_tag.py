import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.article import Article
    from app.models.tag import Tag


class ArticleTag(Base):
    __tablename__ = "article_tags"
    __table_args__ = (
        UniqueConstraint(
            "article_id", "tag_id", name="uq_article_tags_article_id_tag_id"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    tag_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tags.id"), nullable=False
    )
    article_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("articles.id"), nullable=False
    )

    tag: Mapped["Tag"] = relationship("Tag", back_populates="article_tags")
    article: Mapped["Article"] = relationship("Article", back_populates="article_tags")
