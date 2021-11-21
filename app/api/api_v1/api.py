from fastapi import APIRouter

from .endpoints import auth, users, ping

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(ping.router)
