import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.comment import Comment


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, comment: Comment) -> Comment:
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)

        return comment

    def count_article_comments(self, article_id: uuid.UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(Comment)
            .where(Comment.article_id == article_id, Comment.deleted_at.is_(None))
        )

        return self.db.scalar(stmt) or 0

    def list_article_comments(
        self, offset: int, limit: int, article_id: uuid.UUID
    ) -> list[Comment]:
        stmt = (
            select(Comment)
            .options(
                selectinload(Comment.user),
            )
            .where(Comment.article_id == article_id, Comment.deleted_at.is_(None))
            .order_by(Comment.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        return self.db.scalars(stmt).all()

    def get_comment_by_id(self, comment_id: uuid.UUID) -> Comment | None:
        stmt = (
            select(Comment)
            .options(
                selectinload(Comment.user),
                selectinload(Comment.article),
            )
            .where(Comment.id == comment_id, Comment.deleted_at.is_(None))
        )

        return self.db.scalar(stmt)

    def count_user_comments(self, user_id: uuid.UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(Comment)
            .where(Comment.user_id == user_id, Comment.deleted_at.is_(None))
        )

        return self.db.scalar(stmt) or 0

    def list_user_comments(
        self, offset: int, limit: int, user_id: uuid.UUID
    ) -> list[Comment]:
        stmt = (
            select(Comment)
            .options(
                selectinload(Comment.article),
            )
            .where(Comment.user_id == user_id, Comment.deleted_at.is_(None))
            .order_by(Comment.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        return self.db.scalars(stmt).all()
