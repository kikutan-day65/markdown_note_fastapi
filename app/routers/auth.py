from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.exceptions import AuthenticationException
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
    access_token = service.create_token(data=data, token_kind="access")
    refresh_token = service.create_token(data=data, token_kind="refresh")

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )
