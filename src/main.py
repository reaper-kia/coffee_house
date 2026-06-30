from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infra.database.health import check_database_connection
from src.shared.infra.database.session import get_async_session
from src.shared.infra.redis.client import close_redis_client
from src.shared.infra.redis.dependencies import get_redis_client
from src.shared.infra.redis.health import check_redis_connection

@asynccontextmanager
async def lifspan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await close_redis_client()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Coffee House",
        lifespan=lifspan,
    )
    
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "success"}
    
    @app.get("/health/db")
    async def database_health_check(
        session: AsyncSession = Depends(get_async_session)
    ) -> dict[str, str]:
        is_connected = await check_database_connection(session)
        
        if is_connected:
            return {"database": "ok"}
        
        return {"database": "error"}
    
    @app.get("/health/redis")
    async def redis_health_check(
        redis: Redis = Depends(get_redis_client),
    ) -> dict[str, str]:
        is_connected = await check_redis_connection(redis)
        
        if is_connected:
            return {"redis": "ok"}
        
        return {"redis": "error"}
    
    return app

app = create_app()