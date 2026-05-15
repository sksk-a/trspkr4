import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app, reset_users_state


@pytest.fixture(autouse=True)
def clean_users_state():
    reset_users_state()
    yield
    reset_users_state()


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
