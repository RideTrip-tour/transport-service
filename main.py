import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI
from internal_middleware import (
    build_request_id_middleware,
    build_user_context_middleware,
)

from app.clients.gateway_client import GatewayClient
from app.routes.admin_routes import router as admin_router
from app.routes.transport_routes import router as transport_router
from app.utils.logging import LOGGING_CONFIG
from config import settings

logging.config.dictConfig(LOGGING_CONFIG)


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("transport-service is starting up...")
    yield
    await GatewayClient().close()
    logger.info("transport-service is shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        docs_url=f"/api/{settings.app_name.split('-')[0]}/docs",
        redoc_url=f"/api/{settings.app_name.split('-')[0]}/redoc",
        openapi_url=f"/api/{settings.app_name.split('-')[0]}/openapi.json",
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.middleware("http")(build_request_id_middleware(logger=logger))
    app.middleware("http")(build_user_context_middleware(logger=logger))

    @app.get(f"/api/{settings.app_name.split('-')[0]}/health")
    async def health_check():
        return {"status": "ok"}

    # Подключаем пользовательские роутеры
    app.include_router(transport_router)
    # Подключаем администратоские роутеры
    app.include_router(admin_router)

    return app


app = create_app()
