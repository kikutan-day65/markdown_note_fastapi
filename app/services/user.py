import uuid

from app.core.security import get_password_hash
from app.db.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


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
