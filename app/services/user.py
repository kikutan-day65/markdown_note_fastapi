import uuid
from datetime import datetime, timezone

from app.core.exceptions import PermissionDeniedException, UserNotFoundException
from app.core.security import get_password_hash
from app.db.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_data: UserCreate) -> User:
        user_in = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            avatar_url=user_data.avatar_url,
        )

        new_user = self.repository.save(user_in)

        return new_user

    def list_users(self) -> list[User]:
        users = self.repository.get_all()

        return users

    def retrieve_user(self, user_id: uuid.UUID) -> User:
        target = self.repository.get_by_id(user_id)

        if not target:
            raise UserNotFoundException()

        return target

    def update_user(
        self, user_id: uuid.UUID, user_data: UserUpdate, current_user: User
    ) -> User:
        target = self.repository.get_by_id(user_id)

        if not target:
            raise UserNotFoundException()

        if not current_user.is_admin and current_user.id != target.id:
            raise PermissionDeniedException()

        update_data = user_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(target, field, value)

        updated_user = self.repository.save(target)

        return updated_user

    def delete_user(self, user_id: uuid.UUID, current_user: User) -> None:
        target = self.repository.get_by_id(user_id)

        if not target:
            raise UserNotFoundException()

        if not current_user.is_admin and current_user.id != target.id:
            raise PermissionDeniedException()

        # Has target been already deleted?
        if target.deleted_at is not None:
            return

        target.deleted_at = datetime.now(tz=timezone.utc)
        self.repository.save(target)
