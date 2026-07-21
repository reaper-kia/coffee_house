from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

# Импорт роутеров модулей
from src.modules.users.api.router import router as users_router
from src.modules.auth.api.router import router as auth_router
from src.modules.admin.api.router import router as admin_router
from src.modules.catalog.api.router import (
    router as catalog_router,
    admin_router as catalog_admin_router,
)
from src.modules.customer_requests.api.router import (
    router as customer_requests_router,
)

from src.shared.infra.database.health import check_database_connection
from src.shared.infra.database.session import get_async_session
from src.shared.infra.redis.client import close_redis_client
from src.shared.infra.redis.dependencies import get_redis_client
from src.shared.infra.redis.health import check_redis_connection


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await close_redis_client()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Coffee House",
        lifespan=lifespan,
    )

    app.include_router(users_router)
    app.include_router(auth_router)
    app.include_router(admin_router)
    app.include_router(catalog_router, prefix="/api/v1")
    app.include_router(catalog_admin_router, prefix="/api/v1")
    app.include_router(customer_requests_router, prefix="/api/v1",)
    
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "success"}

    @app.get("/health/db")
    async def database_health_check(
        session: AsyncSession = Depends(get_async_session),
    ) -> dict[str, str]:
        is_connected = await check_database_connection(session)
        return {"database": "ok" if is_connected else "error"}

    @app.get("/health/redis")
    async def redis_health_check(
        redis: Redis = Depends(get_redis_client),
    ) -> dict[str, str]:
        is_connected = await check_redis_connection(redis)
        return {"redis": "ok" if is_connected else "error"}

    return app


app = create_app()