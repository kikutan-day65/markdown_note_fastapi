from datetime import datetime, timedelta, timezone

import jwt

from app.core.security import DUMMY_HASH, verify_password
from app.core.settings import settings
from app.db.models.user import User
from app.repositories.auth import AuthRepository


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def authenticate_user(self, identifier: str, password: str) -> User | None:
        if not identifier or not password:
            return None

        target = self.repository.get_user_by_identifier(identifier)

        if not target:
            verify_password(password, DUMMY_HASH)  # To Avoid timing-attack
            return None

        if not verify_password(password, target.password_hash):
            return None

        return target

    def create_token(
        self, data: dict, token_kind: str, expires_delta: timedelta | None = None
    ) -> str:

        to_encode = data.copy()

        now = datetime.now(timezone.utc)
        if token_kind == "access":
            expires_delta = expires_delta or timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            expire = now + expires_delta
        elif token_kind == "refresh":
            expires_delta = expires_delta or timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )
            expire = now + expires_delta
        else:
            raise ValueError("Invalid token kind")

        to_encode.update(
            {
                "type": token_kind,  # access/refresh
                "exp": expire,  # token expiration time
                "iat": now,  # token issued time
            }
        )
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

        return encoded_jwt
