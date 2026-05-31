import uuid
from datetime import datetime, timezone

from app.core.exceptions import (
    PermissionDeniedException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_data: UserCreate) -> User:
        # Unique constraint violation check
        existing_user = self.repository.get_by_username_or_email(
            username=user_data.username, email=user_data.email
        )

        if existing_user:
            raise UserAlreadyExistsException()

        user_in = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            avatar_url=user_data.avatar_url,
        )

        return self.repository.save(user_in)

    def list_users(self) -> list[User]:
        return self.repository.get_all()

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

        is_admin = current_user.is_admin
        is_owner = current_user.id == target.id

        if not is_admin and not is_owner:
            raise PermissionDeniedException()

        update_data = user_data.model_dump(exclude_unset=True)

        # Unique constraint violation check
        if "username" in update_data:
            existing_user = self.repository.get_by_username(
                username=update_data["username"]
            )

            if existing_user and existing_user.id != target.id:
                raise UserAlreadyExistsException()

        for field, value in update_data.items():
            setattr(target, field, value)

        updated_user = self.repository.save(target)

        return updated_user

    def delete_user(self, user_id: uuid.UUID, current_user: User) -> None:
        target = self.repository.get_by_id(user_id)

        if not target:
            raise UserNotFoundException()

        is_admin = current_user.is_admin
        is_owner = current_user.id == target.id

        if not is_admin and not is_owner:
            raise PermissionDeniedException()

        target.deleted_at = datetime.now(tz=timezone.utc)
        self.repository.save(target)
