import uuid

from sqlalchemy import func, select

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(
            User.username == username,
            User.deleted_at.is_(None),
        )

        return self.db.scalar(stmt)

    def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(
            User.email == email,
            User.deleted_at.is_(None),
        )

        return self.db.scalar(stmt)

    def count_users(self) -> int:
        stmt = select(func.count()).select_from(User).where(User.deleted_at.is_(None))

        return self.db.scalar(stmt) or 0

    def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).where(User.id == user_id, User.deleted_at.is_(None))

        return self.db.scalar(stmt)
