import uuid

from sqlalchemy import or_, select

from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.repositories.base import BaseRepository


class AuthRepository(BaseRepository):
    def get_user_by_identifier(self, identifier: str) -> User | None:
        stmt = select(User).where(
            or_(
                User.username == identifier,
                User.email == identifier,
            ),
            User.deleted_at.is_(None),
        )

        return self.db.scalar(stmt)

    def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).where(
            User.id == user_id,
            User.deleted_at.is_(None),
        )

        return self.db.scalar(stmt)

    def get_refresh_token_by_jti(self, jti: uuid.UUID) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.jti == jti)

        return self.db.scalar(stmt)
