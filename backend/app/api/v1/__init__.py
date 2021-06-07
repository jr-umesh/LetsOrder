from fastapi import APIRouter

from .user import routers as user_router
from .menu import routers as menu_router
from .order import routers as order_router

router = APIRouter()

router.include_router(user_router.router, prefix="/users", tags=["User"])
router.include_router(menu_router.router, prefix="/menus", tags=["Menu"])
router.include_router(order_router.router, prefix="/orders", tags=["Order"])
