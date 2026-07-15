import uuid
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    CredentialException,
    InactiveUserException,
)
from app.core.settings import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.repositories.article import ArticleRepository
from app.repositories.auth import AuthRepository
from app.repositories.comment import CommentRepository
from app.repositories.like import LikeRepository
from app.repositories.tag import TagRepository
from app.repositories.user import UserRepository
from app.services.article import ArticleService
from app.services.auth import AuthService
from app.services.comment import CommentService
from app.services.like import LikeService
from app.services.tag import TagService
from app.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

OAuth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DatabaseSession = Annotated[Session, Depends(get_db)]


# ===============================================
# Repository
# ===============================================
def get_user_repository(db: DatabaseSession) -> UserRepository:
    return UserRepository(db=db)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_article_repository(db: DatabaseSession) -> ArticleRepository:
    return ArticleRepository(db=db)


ArticleRepositoryDep = Annotated[ArticleRepository, Depends(get_article_repository)]


def get_comment_repository(db: DatabaseSession) -> CommentRepository:
    return CommentRepository(db=db)


CommentRepositoryDep = Annotated[CommentRepository, Depends(get_comment_repository)]


def get_tag_repository(db: DatabaseSession) -> TagRepository:
    return TagRepository(db=db)


TagRepositoryDep = Annotated[TagRepository, Depends(get_tag_repository)]


def get_like_repository(db: DatabaseSession) -> LikeRepository:
    return LikeRepository(db=db)


LikeRepositoryDep = Annotated[LikeRepository, Depends(get_like_repository)]


def get_auth_repository(db: DatabaseSession) -> AuthRepository:
    return AuthRepository(db=db)


AuthRepositoryDep = Annotated[AuthRepository, Depends(get_auth_repository)]


# ===============================================
# Service
# ===============================================
def get_user_service(repository: UserRepositoryDep) -> UserService:
    return UserService(repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_article_service(
    article_repository: ArticleRepositoryDep,
    tag_repository: TagRepositoryDep,
    user_repository: UserRepositoryDep,
    like_repository: LikeRepositoryDep,
) -> ArticleService:
    return ArticleService(
        article_repository=article_repository,
        tag_repository=tag_repository,
        user_repository=user_repository,
        like_repository=like_repository,
    )


ArticleServiceDep = Annotated[ArticleService, Depends(get_article_service)]


def get_comment_service(
    comment_repository: CommentRepositoryDep,
    article_repository: ArticleRepositoryDep,
) -> CommentService:
    return CommentService(
        comment_repository=comment_repository,
        article_repository=article_repository,
    )


CommentServiceDep = Annotated[CommentService, Depends(get_comment_service)]


def get_tag_service(repository: TagRepositoryDep) -> TagService:
    return TagService(repository)


TagServiceDep = Annotated[TagService, Depends(get_tag_service)]


def get_like_service(
    like_repository: LikeRepositoryDep,
    article_repository: ArticleRepositoryDep,
) -> LikeService:
    return LikeService(
        like_repository=like_repository,
        article_repository=article_repository,
    )


LikeServiceDep = Annotated[LikeService, Depends(get_like_service)]


def get_auth_service(repository: AuthRepositoryDep) -> AuthService:
    return AuthService(repository)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


# ===============================================
# Auth
# ===============================================
def get_current_user(
    token: OAuth2SchemeDep,
    repository: AuthRepositoryDep,
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        if payload.get("type") != "access":
            raise CredentialException()

        user_id = payload.get("sub")
        if not user_id:
            raise CredentialException()

        user_id = uuid.UUID(user_id)

    except (InvalidTokenError, ValueError):
        raise CredentialException()

    user = repository.get_user_by_id(user_id)

    if not user:
        raise CredentialException()

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_current_active_user(current_user: CurrentUserDep) -> User:
    if not current_user.is_active:
        raise InactiveUserException()
    return current_user


CurrentActiveUserDep = Annotated[User, Depends(get_current_active_user)]
