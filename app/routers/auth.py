from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.auth import AuthRepository
from app.schemas.auth import Token
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    repository = AuthRepository(db)
    service = AuthService(repository)

    return service.login(form_data=form_data)


@router.post("/refresh")
def refresh(refresh_token: str, db: Session = Depends(get_db)) -> Token:
    repository = AuthRepository(db)
    service = AuthService(repository)

    return service.refresh(token=refresh_token)


@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    repository = AuthRepository(db)
    service = AuthService(repository)

    service.logout(refresh_token)
