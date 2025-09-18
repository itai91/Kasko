from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .logging_config import configure_logging
from .db.mongo import connect_to_mongo, close_mongo_connection
from .routes import api_router


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="KasKo Life Insurance API", version="0.1.0")

    # CORS – restrict to configured origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def _startup() -> None:
        await connect_to_mongo()

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        await close_mongo_connection()

    app.include_router(api_router, prefix="/api")
    return app


app = create_app()

