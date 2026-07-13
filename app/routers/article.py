import uuid

from fastapi import APIRouter, Query, status

from app.api.deps import (
    ArticleServiceDep,
    CommentServiceDep,
    CurrentActiveUserDep,
    LikeServiceDep,
)
from app.models.article import Article
from app.models.comment import Comment
from app.schemas.article import (
    ArticleCreate,
    ArticlePublic,
    ArticleSummaryWithUser,
    ArticleUpdate,
)
from app.schemas.comment import CommentCreate, CommentPublic, CommentSummaryWithUser
from app.schemas.pagination import PaginatedResponse

router = APIRouter(tags=["articles"])


@router.post(
    "",
    response_model=ArticlePublic,
    status_code=status.HTTP_201_CREATED,
    name="create_article",
)
def create_article(
    current_user: CurrentActiveUserDep,
    service: ArticleServiceDep,
    article_data: ArticleCreate,
) -> Article:
    return service.create_article(current_user=current_user, article_data=article_data)


@router.get(
    "",
    response_model=PaginatedResponse[ArticleSummaryWithUser],
    status_code=status.HTTP_200_OK,
    name="list_articles",
)
def list_articles(
    service: ArticleServiceDep,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> PaginatedResponse[ArticleSummaryWithUser]:
    return service.list_articles(page=page, page_size=page_size)


@router.get(
    "/{article_id}",
    response_model=ArticlePublic,
    status_code=status.HTTP_200_OK,
    name="retrieve_article",
)
def retrieve_article(service: ArticleServiceDep, article_id: uuid.UUID):
    return service.retrieve_article(article_id=article_id)


@router.patch(
    "/{article_id}",
    response_model=ArticlePublic,
    status_code=status.HTTP_200_OK,
    name="update_article",
)
def update_article(
    current_user: CurrentActiveUserDep,
    service: ArticleServiceDep,
    article_id: uuid.UUID,
    article_data: ArticleUpdate,
) -> Article:
    return service.update_article(
        article_id=article_id, user=current_user, article_data=article_data
    )


@router.delete(
    "/{article_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="delete_article",
)
def delete_article(
    current_user: CurrentActiveUserDep,
    service: ArticleServiceDep,
    article_id: uuid.UUID,
) -> None:
    return service.delete_article(user=current_user, article_id=article_id)


@router.post(
    "/{article_id}/like",
    status_code=status.HTTP_204_NO_CONTENT,
    name="like_article",
)
def like_article(
    current_user: CurrentActiveUserDep, article_id: uuid.UUID, service: LikeServiceDep
) -> None:
    return service.like_article(user=current_user, article_id=article_id)


@router.delete(
    "/{article_id}/unlike",
    status_code=status.HTTP_204_NO_CONTENT,
    name="unlike_article",
)
def unlike_article(
    current_user: CurrentActiveUserDep, article_id: uuid.UUID, service: LikeServiceDep
) -> None:
    return service.unlike_article(user=current_user, article_id=article_id)


@router.post(
    "/{article_id}/comments",
    response_model=CommentPublic,
    status_code=status.HTTP_201_CREATED,
    name="create_comment",
)
def create_comment(
    current_user: CurrentActiveUserDep,
    article_id: uuid.UUID,
    comment_data: CommentCreate,
    service: CommentServiceDep,
) -> Comment:
    return service.create_comment(
        user=current_user, article_id=article_id, comment_data=comment_data
    )


@router.get(
    "/{article_id}/comments",
    response_model=PaginatedResponse[CommentSummaryWithUser],
    status_code=status.HTTP_200_OK,
    name="list_article_comments",
)
def list_article_comments(
    service: CommentServiceDep,
    article_id: uuid.UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> PaginatedResponse[CommentSummaryWithUser]:
    return service.list_article_comments(
        page=page, page_size=page_size, article_id=article_id
    )
