import uuid
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.exceptions import (
    AuthenticationException,
    CredentialException,
)
from app.core.settings import settings
from app.repositories.auth import AuthRepository
from app.schemas.auth import Token
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    repository = AuthRepository(db)
    service = AuthService(repository)

    identifier = form_data.username  # put username/email to identifier
    user = service.authenticate_user(identifier, form_data.password)

    if not user:
        raise AuthenticationException()

    data = {"sub": str(user.id)}
    access_token, _ = service.create_token(data=data, token_kind="access")
    refresh_token, expire = service.create_token(data=data, token_kind="refresh")

    service.save_refresh_token(user_id=user.id, token=refresh_token, expire=expire)

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/refresh")
def refresh(refresh_token: str, db: Session = Depends(get_db)) -> Token:
    repository = AuthRepository(db)
    service = AuthService(repository)

    return service.refresh(token=refresh_token)


@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    repository = AuthRepository(db)
    service = AuthService(repository)

    try:
        # Decode refresh token
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        # Check 'type: refresh'
        if payload.get("type") != "refresh":
            raise CredentialException()

        # Check 'sub: uuid'
        user_id = payload.get("sub")
        if not user_id:
            raise CredentialException()

        user_id = uuid.UUID(user_id)

    except (InvalidTokenError, ValueError):
        raise CredentialException()

    # Check user_id exists in db
    user = repository.get_user_by_id(user_id)
    if not user:
        raise CredentialException()

    # Revoke old refresh token
    service.revoke_refresh_token(user.id, refresh_token)

    # Generate access/refresh token
    data = {"sub": str(user.id)}
    new_access_token, _ = service.create_token(data=data, token_kind="access")
    new_refresh_token, expire = service.create_token(data=data, token_kind="refresh")

    # Save new refresh token
    service.save_refresh_token(user_id=user.id, token=new_refresh_token, expire=expire)

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )
