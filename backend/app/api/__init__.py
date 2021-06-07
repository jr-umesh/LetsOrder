from fastapi import APIRouter
from . import v1
from app.api.shared.auth import routers as auth_routers

router = APIRouter()
router.include_router(v1.router)
router.include_router(auth_routers.router, prefix='/auth', tags=["Auth"])
