from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.db.init_db import init_db
from app.api import router


def append_routes(app):
    app.include_router(router, prefix=settings.API_PREFIX)


def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        version=1.0
    )

    app.mount(settings.STATIC_URL, StaticFiles(
        directory=settings.STATIC_PATH), name="static")

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in
                           settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # initialize database
    init_db()

    append_routes(app)

    return app


app = create_app()
