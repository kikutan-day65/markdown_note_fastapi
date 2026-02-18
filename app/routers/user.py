import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_password_hash
from app.db.models.user import User
from app.schemas.user import UserAdmin, UserCreate, UserPublic

router = APIRouter()


@router.post("/users", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password),
        avatar_url=user.avatar_url,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/users", response_model=list[UserAdmin])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return users


@router.get("/user/{id}", response_model=UserPublic)
def get_user(id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.get(User, id)

    return user
