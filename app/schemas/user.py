import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.schemas.base import ORMBase


# ===== REQUEST =====
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    avatar_url: str | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    avatar_url: str | None = None


class UserChangeEmail(BaseModel):
    email: EmailStr


class UserChangePassword(BaseModel):
    current_password: str
    new_password: str


# ===== RESPONSE =====
class UserPublic(ORMBase):
    id: uuid.UUID
    username: str
    avatar_url: str | None
    created_at: datetime
    updated_at: datetime


class UserAdmin(ORMBase):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_admin: bool
    is_active: bool
    is_verified: bool
    avatar_url: str | None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
    last_login: datetime | None


class UserMe(ORMBase):
    id: uuid.UUID
    username: str
    email: EmailStr
    avatar_url: str | None
    created_at: datetime
    updated_at: datetime
