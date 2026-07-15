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
    old_email: EmailStr
    new_email: EmailStr


class UserChangePassword(BaseModel):
    current_password: str
    new_password: str


# ===== RESPONSE =====
class UserPrivate(ORMBase):
    id: uuid.UUID
    username: str
    email: EmailStr
    avatar_url: str | None
    created_at: datetime
    updated_at: datetime


class UserPublic(ORMBase):
    id: uuid.UUID
    username: str
    avatar_url: str | None
    created_at: datetime
    updated_at: datetime


class UserSummary(ORMBase):
    id: uuid.UUID
    username: str
