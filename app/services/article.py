import uuid
from datetime import datetime, timezone
from math import ceil

from app.core.exceptions import (
    ArticleNotFoundException,
    PermissionDeniedException,
    TagNotFoundException,
    UserNotFoundException,
)
from app.models.article import Article
from app.models.user import User
from app.repositories.article import ArticleRepository
from app.repositories.like import LikeRepository
from app.repositories.tag import TagRepository
from app.repositories.user import UserRepository
from app.schemas.article import (
    ArticleCreate,
    ArticleSummaryWithoutUser,
    ArticleSummaryWithUser,
    ArticleUpdate,
)
from app.schemas.pagination import PaginatedResponse


class ArticleService:
    def __init__(
        self,
        article_repository: ArticleRepository,
        tag_repository: TagRepository,
        user_repository: UserRepository,
        like_repository: LikeRepository,
    ):
        self.article_repository = article_repository
        self.tag_repository = tag_repository
        self.user_repository = user_repository
        self.like_repository = like_repository

    def create_article(
        self, current_user: User, article_data: ArticleCreate
    ) -> Article:
        article = Article(
            title=article_data.title,
            content=article_data.content,
            user_id=current_user.id,
        )

        tag_ids = set(article_data.tag_ids)
        tags = self.tag_repository.get_tags_by_ids(tag_ids)

        if len(tags) != len(tag_ids):
            raise TagNotFoundException()

        article.tags = tags

        return self.article_repository.save(article)

    def list_articles(
        self, page: int, page_size: int
    ) -> PaginatedResponse[ArticleSummaryWithUser]:
        offset = (page - 1) * page_size
        total = self.article_repository.count_articles()
        total_pages = ceil(total / page_size)

        articles = self.article_repository.list_articles(offset=offset, limit=page_size)

        article_ids = [article.id for article in articles]
        likes_count_dict = self.like_repository.count_likes_by_article_ids(
            article_ids=article_ids
        )

        for article in articles:
            likes_count_by_article = likes_count_dict.get(article.id, 0)
            article.likes_count = likes_count_by_article

        return PaginatedResponse(
            items=articles,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )

    def retrieve_article(self, article_id: uuid.UUID) -> Article:
        article = self.article_repository.get_article_by_id(article_id=article_id)

        if not article:
            raise ArticleNotFoundException()

        likes_count_int = self.like_repository.count_likes_by_article_id(
            article_id=article_id
        )

        article.likes_count = likes_count_int

        return article

    def update_article(
        self, article_id: uuid.UUID, user: User, article_data: ArticleUpdate
    ) -> Article:
        article = self.article_repository.get_article_by_id(article_id=article_id)

        if not article:
            raise ArticleNotFoundException()

        if article.user_id != user.id:
            raise PermissionDeniedException()

        update_data = article_data.model_dump(exclude_unset=True)

        tag_ids = update_data.pop("tag_ids", None)

        for field, value in update_data.items():
            setattr(article, field, value)

        if tag_ids is not None:
            tag_ids_set = set(tag_ids)
            tags = self.tag_repository.get_tags_by_ids(tag_ids_set)

            if len(tags) != len(tag_ids_set):
                raise TagNotFoundException()

            article.tags = tags

        return self.article_repository.save(article)

    def delete_article(self, user: User, article_id: uuid.UUID) -> None:
        article = self.article_repository.get_article_by_id(article_id=article_id)

        if not article:
            raise ArticleNotFoundException()

        if article.user_id != user.id:
            raise PermissionDeniedException()

        article.deleted_at = datetime.now(tz=timezone.utc)

        self.article_repository.save(article)

        # commentは論理削除しなくてもよい？
        # なぜならば、commentは記事作成者以外がしているので
        # 記事が削除されたら別ユーザのcommentが論理削除されてしまうのはおかしい

    def list_user_articles(
        self, page: int, page_size: int, user_id: uuid.UUID
    ) -> PaginatedResponse[ArticleSummaryWithoutUser]:
        user = self.user_repository.get_user_by_id(user_id=user_id)

        if not user:
            raise UserNotFoundException()

        offset = (page - 1) * page_size
        total = self.article_repository.count_user_articles(user_id=user_id)
        total_pages = ceil(total / page_size)

        articles = self.article_repository.list_user_articles(
            offset=offset, limit=page_size, user_id=user_id
        )

        article_ids = [article.id for article in articles]
        likes_count_dict = self.like_repository.count_likes_by_article_ids(
            article_ids=article_ids
        )

        for article in articles:
            likes_count_by_article = likes_count_dict.get(article.id, 0)
            article.likes_count = likes_count_by_article

        return PaginatedResponse(
            items=articles,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )
