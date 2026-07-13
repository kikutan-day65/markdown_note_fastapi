import uuid

from fastapi import APIRouter, Query, status

from app.api.deps import (
    ArticleServiceDep,
    CommentServiceDep,
    CurrentActiveUserDep,
    UserServiceDep,
)
from app.models.user import User
from app.schemas.article import ArticleSummaryWithoutUser
from app.schemas.comment import CommentSummaryWithArticle
from app.schemas.pagination import PaginatedResponse
from app.schemas.user import UserCreate, UserPrivate, UserPublic, UserUpdate

router = APIRouter(tags=["users"])


@router.get(
    "/me",
    response_model=UserPrivate,
    status_code=status.HTTP_200_OK,
    name="get_me",
)
def get_me(current_user: CurrentActiveUserDep) -> User:
    return current_user


@router.patch(
    "/me",
    response_model=UserPrivate,
    status_code=status.HTTP_200_OK,
    name="update_me",
)
def update_me(
    current_user: CurrentActiveUserDep, service: UserServiceDep, user_data: UserUpdate
) -> User:
    return service.update_me(current_user=current_user, user_data=user_data)


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    name="delete_me",
)
def delete_me(current_user: CurrentActiveUserDep, service: UserServiceDep) -> None:
    return service.delete_me(current_user=current_user)


@router.get(
    "/me/articles",
    response_model=PaginatedResponse[ArticleSummaryWithoutUser],
    status_code=status.HTTP_200_OK,
    name="list_my_articles",
)
def list_my_articles(
    current_user: CurrentActiveUserDep,
    service: ArticleServiceDep,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> PaginatedResponse[ArticleSummaryWithoutUser]:
    return service.list_user_articles(
        page=page, page_size=page_size, user_id=current_user.id
    )


@router.get(
    "/me/comments",
    response_model=PaginatedResponse[CommentSummaryWithArticle],
    status_code=status.HTTP_200_OK,
    name="list_my_comments",
)
def list_my_comments(
    current_user: CurrentActiveUserDep,
    service: CommentServiceDep,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> PaginatedResponse[CommentSummaryWithArticle]:
    return service.list_user_comments(
        page=page, page_size=page_size, user_id=current_user.id
    )


# PATCH /me/change-email
# PATCH /me/change-password


@router.post(
    "",
    response_model=UserPrivate,
    status_code=status.HTTP_201_CREATED,
    name="create_user",
)
def create_user(user_data: UserCreate, service: UserServiceDep) -> User:
    return service.create_user(user_data=user_data)


@router.get(
    "/{user_id}",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
    name="retrieve_user",
)
def retrieve_user(service: UserServiceDep, user_id: uuid.UUID) -> User:
    return service.retrieve_user(user_id=user_id)


@router.get(
    "/{user_id}/articles",
    response_model=PaginatedResponse[ArticleSummaryWithoutUser],
    status_code=status.HTTP_200_OK,
    name="list_user_articles",
)
def list_user_articles(
    service: ArticleServiceDep,
    user_id: uuid.UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> PaginatedResponse[ArticleSummaryWithoutUser]:
    return service.list_user_articles(page=page, page_size=page_size, user_id=user_id)
