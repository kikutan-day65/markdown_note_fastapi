import uuid
from datetime import datetime, timezone

from app.core.exceptions import (
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
        # Is username unique in db?
        if self.repository.get_user_by_username(username=user_data.username):
            raise UserAlreadyExistsException()

        # Is email unique in db?
        if self.repository.get_user_by_email(email=user_data.email):
            raise UserAlreadyExistsException()

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            avatar_url=user_data.avatar_url,
        )

        return self.repository.save(new_user)

    def retrieve_user(self, user_id: uuid.UUID) -> User:
        user = self.repository.get_user_by_id(user_id=user_id)

        if not user:
            raise UserNotFoundException()

        return user

    def update_me(self, current_user: User, user_data: UserUpdate) -> User:
        if user_data.username:
            existing_user = self.repository.get_user_by_username(
                username=user_data.username
            )

            if existing_user and existing_user.id != current_user.id:
                raise UserAlreadyExistsException()

        update_data = user_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(current_user, field, value)

        return self.repository.save(current_user)

    def delete_me(self, current_user: User) -> None:
        now = datetime.now(tz=timezone.utc)

        current_user.deleted_at = now
        self.repository.save(current_user)

        # refresh token, article, like, commentを
        # 論理削除する必要がある。
