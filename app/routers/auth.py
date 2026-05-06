from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import AuthServiceDep
from app.schemas.auth import RefreshTokenRequest, Token

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token, status_code=200, name="login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep,
) -> Token:
    return service.login(form_data=form_data)


@router.post("/refresh", response_model=Token, status_code=200, name="refresh")
def refresh(request: RefreshTokenRequest, service: AuthServiceDep) -> Token:
    return service.refresh(token=request.refresh_token)


@router.post("/logout", status_code=204, name="logout")
def logout(request: RefreshTokenRequest, service: AuthServiceDep):
    service.logout(request.refresh_token)
