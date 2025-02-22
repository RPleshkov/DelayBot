from aiogram import Router
from .other import router as other_router
from .user import router as user_router

__all__ = [
    "routers",
]


def routers() -> list[Router]:
    return [user_router, other_router]
