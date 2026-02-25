import uuid

from sqlalchemy.orm import Session

from app.db.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_all(self) -> list[User]:
        return self.db.query(User).all()

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return (
            self.db.query(User)
            .filter(
                User.id == user_id,
                User.deleted_at.is_(None),
            )
            .first()
        )
