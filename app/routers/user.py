import uuid

from fastapi import APIRouter, status

from app.api.deps import CurrentActiveUserDep, CurrentAdminUserDep, UserServiceDep
from app.models.user import User
from app.schemas.user import UserAdmin, UserCreate, UserMe, UserPublic, UserUpdate

router = APIRouter(tags=["users"])


@router.get(
    "/me",
    response_model=UserMe,
    status_code=status.HTTP_200_OK,
    name="read_me",
)
def read_me(current_user: CurrentActiveUserDep) -> User:
    return current_user


@router.post(
    "",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    name="create_user",
)
def create_user(user: UserCreate, service: UserServiceDep) -> User:
    return service.create_user(user)


@router.get(
    "",
    response_model=list[UserAdmin],
    status_code=status.HTTP_200_OK,
    name="list_users",
)
def list_users(_: CurrentAdminUserDep, service: UserServiceDep) -> list[User]:
    return service.list_users()


@router.get(
    "/{id}", response_model=UserPublic, status_code=status.HTTP_200_OK, name="get_user"
)
def get_user(id: uuid.UUID, service: UserServiceDep) -> User:
    return service.retrieve_user(id)


@router.patch(
    "/{id}",
    response_model=UserAdmin,
    status_code=status.HTTP_200_OK,
    name="update_user",
)
def update_user(
    id: uuid.UUID,
    user: UserUpdate,
    current_user: CurrentActiveUserDep,
    service: UserServiceDep,
) -> User:
    return service.update_user(id, user, current_user)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="delete_user",
)
def delete_user(
    id: uuid.UUID,
    current_user: CurrentActiveUserDep,
    service: UserServiceDep,
) -> None:
    service.delete_user(id, current_user)
