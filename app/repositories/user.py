import uuid

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_all(self) -> list[User]:
        stmt = select(User).where(User.deleted_at.is_(None))
        return self.db.scalars(stmt).all()

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).where(
            User.id == user_id,
            User.deleted_at.is_(None),
        )
        return self.db.scalar(stmt)

    def get_by_username_or_email(self, username: str, email: str) -> User | None:
        stmt = select(User).where(
            or_(
                User.username == username,
                User.email == email,
            ),
            User.deleted_at.is_(None),
        )

        return self.db.scalar(stmt)

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(
            User.username == username,
            User.deleted_at.is_(None),
        )

        return self.db.scalar(stmt)
