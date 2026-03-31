from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.models.user import User


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_identifier(self, identifier: str) -> User | None:
        stmt = select(User).where(
            or_(
                User.username == identifier,
                User.email == identifier,
            ),
            User.deleted_at.is_(None),
        )
        return self.db.scalar(stmt)

    def get_user_by_id(self, user_id) -> User | None:
        stmt = select(User).where(
            User.id == user_id,
            User.deleted_at.is_(None),
        )

        return self.db.scalar(stmt)
