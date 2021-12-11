from fastapi import APIRouter

from .endpoints import auth, users, ping

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(ping.router, tags=["ping"])
