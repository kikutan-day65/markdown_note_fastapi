import uuid

from app.core.exceptions import (
    ArticleAlreadyLikedException,
    ArticleNotFoundException,
    CannotLikeOwnArticleException,
    LikeNotFoundException,
)
from app.models.like import Like
from app.models.user import User
from app.repositories.article import ArticleRepository
from app.repositories.like import LikeRepository


class LikeService:
    def __init__(
        self, like_repository: LikeRepository, article_repository: ArticleRepository
    ):
        self.like_repository = like_repository
        self.article_repository = article_repository

    def like_article(self, user: User, article_id: uuid.UUID) -> None:
        article = self.article_repository.get_article_by_id(article_id=article_id)

        if not article:
            raise ArticleNotFoundException()

        if article.user_id == user.id:
            raise CannotLikeOwnArticleException()

        existing_like = self.like_repository.get_like_by_user_id_and_article_id(
            user_id=user.id, article_id=article_id
        )

        if existing_like:
            raise ArticleAlreadyLikedException()

        like = Like(user_id=user.id, article_id=article_id)

        self.like_repository.save(like)

    def unlike_article(self, user: User, article_id: uuid.UUID) -> None:
        like = self.like_repository.get_like_by_user_id_and_article_id(
            user_id=user.id, article_id=article_id
        )

        if not like:
            raise LikeNotFoundException()

        self.like_repository.delete_like(like)
