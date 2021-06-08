from fastapi import APIRouter

from .endpoints import user, login, menu

router = APIRouter()

router.include_router(user.router, prefix="/users", tags=["User"])
router.include_router(login.router, prefix="/auth", tags=["Auth"])
router.include_router(menu.router, prefix="/menu", tags=["Menu"])
