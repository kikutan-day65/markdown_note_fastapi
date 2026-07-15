from fastapi import APIRouter

from app.routers import article, auth, comment, tag, user

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user.router, prefix="/users")
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(article.router, prefix="/articles")
api_router.include_router(tag.router, prefix="/tags")
api_router.include_router(comment.router, prefix="/comments")
