import uuid
from datetime import datetime, timezone
from math import ceil

from app.core.exceptions import (
    ArticleNotFoundException,
    CommentNotFoundException,
    PermissionDeniedException,
    UserNotFoundException,
)
from app.models.comment import Comment
from app.models.user import User
from app.repositories.article import ArticleRepository
from app.repositories.comment import CommentRepository
from app.schemas.comment import (
    CommentCreate,
    CommentSummaryWithArticle,
    CommentSummaryWithUser,
    CommentUpdate,
)
from app.schemas.pagination import PaginatedResponse


class CommentService:
    def __init__(
        self,
        comment_repository: CommentRepository,
        article_repository: ArticleRepository,
    ):
        self.comment_repository = comment_repository
        self.article_repository = article_repository

    def create_comment(
        self, user: User, article_id: uuid.UUID, comment_data: CommentCreate
    ) -> Comment:
        article = self.article_repository.get_article_by_id(article_id=article_id)

        if not article:
            raise ArticleNotFoundException()

        comment = Comment(
            body=comment_data.body, user_id=user.id, article_id=article_id
        )

        return self.comment_repository.save(comment)

    def list_article_comments(
        self, page: int, page_size: int, article_id: uuid.UUID
    ) -> PaginatedResponse[CommentSummaryWithUser]:
        article = self.article_repository.get_article_by_id(article_id=article_id)

        if not article:
            raise ArticleNotFoundException()

        offset = (page - 1) * page_size
        total = self.comment_repository.count_article_comments(article_id=article_id)
        total_pages = ceil(total / page_size)

        comments = self.comment_repository.list_article_comments(
            offset=offset, limit=page_size, article_id=article_id
        )

        return PaginatedResponse(
            items=comments,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )

    def retrieve_comment(self, comment_id: uuid.UUID) -> Comment:
        comment = self.comment_repository.get_comment_by_id(comment_id=comment_id)

        if not comment:
            raise CommentNotFoundException()

        return comment

    def update_comment(
        self, user: User, comment_id: uuid.UUID, comment_data: CommentUpdate
    ) -> Comment:
        comment = self.comment_repository.get_comment_by_id(comment_id=comment_id)

        if not comment:
            raise CommentNotFoundException()

        if comment.user_id != user.id:
            raise PermissionDeniedException()

        comment.body = comment_data.body

        return self.comment_repository.save(comment)

    def delete_comment(self, user: User, comment_id: uuid.UUID) -> None:
        comment = self.comment_repository.get_comment_by_id(comment_id=comment_id)

        if not comment:
            raise CommentNotFoundException()

        if comment.user_id != user.id:
            raise PermissionDeniedException()

        comment.deleted_at = datetime.now(tz=timezone.utc)

        self.comment_repository.save(comment)

    def list_user_comments(
        self, page: int, page_size: int, user_id: uuid.UUID
    ) -> PaginatedResponse[CommentSummaryWithArticle]:
        user = self.user_repository.get_user_by_id(user_id=user_id)

        if not user:
            raise UserNotFoundException()

        offset = (page - 1) * page_size
        total = self.comment_repository.count_user_comments(user_id=user_id)
        total_pages = ceil(total / page_size)

        comments = self.comment_repository.list_user_comments(
            offset=offset, limit=page_size, user_id=user_id
        )

        return PaginatedResponse(
            items=comments,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )
