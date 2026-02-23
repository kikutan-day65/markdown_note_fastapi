import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserAdmin, UserCreate, UserPublic
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    repository = UserRepository(db)
    service = UserService(repository)

    new_user = service.create_user(user)

    return new_user


@router.get("", response_model=list[UserAdmin])
def list_users(db: Session = Depends(get_db)) -> list[User]:
    repository = UserRepository(db)
    service = UserService(repository)

    users = service.list_users()

    return users


@router.get("/{id}", response_model=UserPublic)
def get_user(id: uuid.UUID, db: Session = Depends(get_db)) -> User:
    repository = UserRepository(db)
    service = UserService(repository)

    user = service.retrieve_user(id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user
