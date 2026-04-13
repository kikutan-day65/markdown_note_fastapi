from fastapi import APIRouter

from app.routers import auth, user

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user.router, prefix="/users")
api_router.include_router(auth.router, prefix="/auth")
