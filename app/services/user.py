import uuid
from datetime import datetime, timezone

from app.core.security import get_password_hash
from app.db.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user: UserCreate) -> User:
        user_in = User(
            username=user.username,
            email=user.email,
            password_hash=get_password_hash(user.password),
            avatar_url=user.avatar_url,
        )

        new_user = self.repository.save(user_in)

        return new_user

    def list_users(self) -> list[User]:
        users = self.repository.get_all()

        return users

    def retrieve_user(self, user_id: uuid.UUID) -> User | None:
        user = self.repository.get_by_id(user_id)

        return user

    def update_user(self, user_id: uuid.UUID, user: UserUpdate) -> User | None:
        target = self.repository.get_by_id(user_id)

        if not target:
            return None

        update_data = user.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(target, field, value)

        updated_user = self.repository.save(target)

        return updated_user

    def delete_user(self, user_id: uuid.UUID) -> User | None:
        target = self.repository.get_by_id(user_id)

        if not target:
            return None

        if target.deleted_at is not None:
            return target

        target.deleted_at = datetime.now(tz=timezone.utc)
        deleted_user = self.repository.save(target)

        return deleted_user
