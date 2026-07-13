import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.article import Article


class ArticleRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, article: Article) -> Article:
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)

        return article

    def count_articles(self) -> int:
        stmt = (
            select(func.count())
            .select_from(Article)
            .where(Article.deleted_at.is_(None))
        )

        return self.db.scalar(stmt) or 0

    def list_articles(self, offset: int, limit: int) -> list[Article]:
        stmt = (
            select(Article)
            .options(
                selectinload(Article.user),
                selectinload(Article.tags),
            )
            .where(Article.deleted_at.is_(None))
            .order_by(Article.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        return self.db.scalars(stmt).all()

    def get_article_by_id(self, article_id: uuid.UUID) -> Article | None:
        stmt = (
            select(Article)
            .options(
                selectinload(Article.user),
                selectinload(Article.tags),
            )
            .where(
                Article.id == article_id,
                Article.deleted_at.is_(None),
            )
        )

        return self.db.scalar(stmt)

    def count_user_articles(self, user_id: uuid.UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(Article)
            .where(Article.user_id == user_id, Article.deleted_at.is_(None))
        )

        return self.db.scalar(stmt) or 0

    def list_user_articles(
        self, offset: int, limit: int, user_id: uuid.UUID
    ) -> list[Article]:
        stmt = (
            select(Article)
            .options(
                selectinload(Article.tags),
            )
            .where(Article.user_id == user_id, Article.deleted_at.is_(None))
            .order_by(Article.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        return self.db.scalars(stmt).all()
