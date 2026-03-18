from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.exceptions import AuthenticationException
from app.repositories.auth import AuthRepository
from app.schemas.auth import LoginRequest, Token
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
def login_for_access_token(
    login_request: LoginRequest,
    db: Session = Depends(get_db),
) -> Token:
    repository = AuthRepository(db)
    service = AuthService(repository)

    user = service.authenticate_user(login_request.identifier, login_request.password)

    if not user:
        raise AuthenticationException()

    data = {"sub": str(user.id)}
    access_token = service.create_token(data=data, token_kind="access")
    refresh_token = service.create_token(data=data, token_kind="refresh")

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )
