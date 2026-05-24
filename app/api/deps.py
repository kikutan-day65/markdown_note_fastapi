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
    PermissionDeniedException,
)
from app.core.settings import settings
from app.db.models import User
from app.db.session import SessionLocal
from app.repositories.auth import AuthRepository
from app.repositories.user import UserRepository
from app.services.auth import AuthService
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


def get_auth_repository(db: DatabaseSession) -> AuthRepository:
    return AuthRepository(db)


AuthRepositoryDep = Annotated[AuthRepository, Depends(get_auth_repository)]


def get_auth_service(repository: AuthRepositoryDep) -> AuthService:
    return AuthService(repository)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_user_repository(db: DatabaseSession) -> UserRepository:
    return UserRepository(db)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(repository: UserRepositoryDep) -> UserService:
    return UserService(repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


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


def get_current_admin_user(
    current_user: CurrentActiveUserDep,
) -> User:
    if not current_user.is_admin:
        raise PermissionDeniedException()
    return current_user


CurrentAdminUserDep = Annotated[User, Depends(get_current_admin_user)]
