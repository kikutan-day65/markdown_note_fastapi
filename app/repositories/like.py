import uuid

from sqlalchemy import func, select

from app.models.like import Like
from app.repositories.base import BaseRepository


class LikeRepository(BaseRepository):
    def get_like_by_user_id_and_article_id(
        self, user_id: uuid.UUID, article_id: uuid.UUID
    ) -> Like | None:
        stmt = select(Like).where(
            Like.user_id == user_id, Like.article_id == article_id
        )

        return self.db.scalar(stmt)

    def delete_like(self, like: Like) -> None:
        self.db.delete(like)

    def count_likes_by_article_id(self, article_id: uuid.UUID) -> int:
        stmt = (
            select(func.count()).select_from(Like).where(Like.article_id == article_id)
        )

        return self.db.scalar(stmt) or 0

    def count_likes_by_article_ids(
        self, article_ids: list[uuid.UUID]
    ) -> dict[uuid.UUID, int]:
        if not article_ids:
            return {}

        stmt = (
            select(
                Like.article_id,
                func.count(),
            )
            .select_from(Like)
            .where(Like.article_id.in_(article_ids))
            .group_by(Like.article_id)
        )

        results = self.db.execute(stmt).all()

        return {article_id: likes_count for article_id, likes_count in results}
