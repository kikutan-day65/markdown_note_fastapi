import uuid
from datetime import datetime, timezone

from app.core.decorator import transactional
from app.core.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.core.security import get_password_hash
from app.core.unit_of_work import UnitOfWork
from app.models.user import User
from app.repositories.like import LikeRepository
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        like_repository: LikeRepository,
        uow: UnitOfWork,
    ):
        self.user_repository = user_repository
        self.like_repository = like_repository
        self.uow = uow

    @transactional
    def create_user(self, user_data: UserCreate) -> User:
        # Is username unique in db?
        if self.user_repository.get_user_by_username(username=user_data.username):
            raise UserAlreadyExistsException()

        # Is email unique in db?
        if self.user_repository.get_user_by_email(email=user_data.email):
            raise UserAlreadyExistsException()

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            avatar_url=user_data.avatar_url,
        )

        self.user_repository.add(new_user)
        self.user_repository.flush()
        self.user_repository.refresh(new_user)

        return new_user

    def retrieve_user(self, user_id: uuid.UUID) -> User:
        user = self.user_repository.get_user_by_id(user_id=user_id)

        if not user:
            raise UserNotFoundException()

        return user

    @transactional
    def update_me(self, current_user: User, user_data: UserUpdate) -> User:
        if user_data.username:
            existing_user = self.user_repository.get_user_by_username(
                username=user_data.username
            )

            # Is username unique in db?
            if existing_user and existing_user.id != current_user.id:
                raise UserAlreadyExistsException()

        update_data = user_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(current_user, field, value)

        self.user_repository.flush()
        self.user_repository.refresh(current_user)

        return current_user

    @transactional
    def delete_me(self, current_user: User) -> None:
        now = datetime.now(tz=timezone.utc)

        # Soft-delete user
        current_user.deleted_at = now

        # Revoke refresh tokens
        refresh_tokens = current_user.refresh_tokens
        for refresh_token in refresh_tokens:
            if refresh_token.revoked_at is None:
                refresh_token.revoked_at = now

        # Soft-delete articles
        articles = current_user.articles
        for article in articles:
            if article.deleted_at is None:
                article.deleted_at = now

        # Soft-delete comments
        comments = current_user.comments
        for comment in comments:
            if comment.deleted_at is None:
                comment.deleted_at = now

        # Delete likes
        likes = current_user.likes
        for like in likes:
            self.like_repository.delete_like(like=like)

        # 削除されたuserが持っているarticleに対して追加された
        # 他userのcommentやlikeはどうする？
