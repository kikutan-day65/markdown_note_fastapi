import uuid
from datetime import datetime, timedelta, timezone

import jwt

from app.core.exceptions import CredentialException
from app.core.security import DUMMY_HASH, get_password_hash, verify_password
from app.core.settings import settings
from app.db.models.refresh_token import RefreshToken
from app.db.models.user import User
from app.repositories.auth import AuthRepository
from app.schemas.auth import Token


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def logout(self, token: str):
        user_id, jti = self.decode_refresh_token(token=token)

        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise CredentialException()

        target = self.repository.get_refresh_token_by_jti(jti=jti)
        if not target:
            raise CredentialException()

        self.revoke_refresh_token(target=target)

    def refresh(self, token: str) -> Token:
        user_id, jti = self.decode_refresh_token(token=token)

        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise CredentialException()

        target = self.repository.get_refresh_token_by_jti(jti=jti)
        if not target:
            raise CredentialException()

        if target.revoked_at is not None:
            raise TokenReuseException()

        self.revoke_refresh_token(target=target)

        data = {"sub": str(user.id)}
        new_access_token, _, _ = self.create_token(data=data, token_kind="access")
        new_refresh_token, expire, jti = self.create_token(
            data=data, token_kind="refresh"
        )

        self.save_refresh_token(
            user_id=user.id,
            token=new_refresh_token,
            expire=expire,
            jti=jti,
        )

        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )

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
    ) -> tuple[str, datetime]:

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

        return encoded_jwt, expire, jti

    def decode_refresh_token(self, token: str) -> tuple[uuid.UUID, uuid.UUID]:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )

            if payload.get("type") != "refresh":
                raise CredentialException()

            user_id = payload.get("sub")
            if not user_id:
                raise CredentialException()
            user_id = uuid.UUID(user_id)

            jti = payload.get("jti")
            if not jti:
                raise CredentialException()
            jti = uuid.UUID(jti)

        except (InvalidTokenError, ValueError):
            raise CredentialException()

        return user_id, jti

    def save_refresh_token(
        self, user_id: uuid.UUID, token: str, expire: datetime
    ) -> None:
        data = RefreshToken(
            user_id=user_id, token=get_password_hash(token), expires_at=expire
        )
        self.repository.save_refresh_token(data)

    def revoke_refresh_token(self, user_id: uuid.UUID, token: str) -> None:
        refresh_tokens = self.repository.get_refresh_tokens(user_id=user_id)

        if not refresh_tokens:
            raise CredentialException()

        target = None

        for rt in refresh_tokens:
            if verify_password(token, rt.token):
                target = rt
                break

        if not target:
            raise CredentialException()

        now = datetime.now(tz=timezone.utc)
        if target.expires_at < now:
            raise CredentialException()

        target.revoked_at = now

        # Update old refresh token -> revoked_at is set
        self.repository.save_refresh_token(target)
