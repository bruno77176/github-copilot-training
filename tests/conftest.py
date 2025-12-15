import asyncio
import pytest
from httpx import AsyncClient

from app.main import app as _app, MOCK_TASKS


@pytest.fixture(scope="session")
def app():
    """Provide FastAPI app for integration tests."""
    return _app


@pytest.fixture
async def client(app):
    """Async HTTP client for integration tests."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def reset_mock_tasks():
    """Reset `MOCK_TASKS` to its initial state after each test that mutates it."""
    original = MOCK_TASKS.copy()
    yield
    MOCK_TASKS.clear()
    MOCK_TASKS.update(original)


@pytest.fixture
def db_session():
    """Placeholder db_session fixture for tests that expect it.

    This project uses an in-memory store; return None to satisfy signatures.
    """
    return None


@pytest.fixture
def auth_token():
    """Return a dummy auth token for endpoints that require auth in future tests."""
    return "test-token"
