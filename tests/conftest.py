import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.main import app
from src.shared.infra.database.base import Base
from src.core.config import settings

# Используем тестовую БД (можно отдельную, можно ту же, но с очисткой)
TEST_DATABASE_URL = "postgresql+asyncpg://coffee_house:coffee_house@localhost:5432/test_db"

@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        # Пересоздаём схему для тестов
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def session(engine):
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Фикстура для получения админского токена (заглушка)
# Для реального теста нужно получить токен через /auth/login
@pytest.fixture
async def admin_token():
    # В реальном проекте можно создать тестового пользователя с правами админа
    # и получить токен через эндпоинт логина.
    # Здесь для простоты возвращаем заглушку, но в тестах можно использовать
    # dependency override для require_admin.
    return "test_admin_token"

# Переопределяем зависимость require_admin для тестов,
# чтобы админские эндпоинты не требовали реальной аутентификации
from src.modules.auth.api.dependencies import require_admin

@pytest.fixture(autouse=True)
def override_require_admin():
    from fastapi import Depends
    async def mock_require_admin():
        return {"id": "test-admin-id", "is_admin": True}
    app.dependency_overrides[require_admin] = mock_require_admin
    yield
    app.dependency_overrides.clear()