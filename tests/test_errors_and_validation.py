import pytest


@pytest.mark.asyncio
async def test_custom_exception_a(async_client):
    response = await async_client.get("/errors/check-age/16")

    assert response.status_code == 400
    data = response.json()
    assert data["error_code"] == "CUSTOM_A"
    assert data["message"] == "Age must be at least 18"


@pytest.mark.asyncio
async def test_custom_exception_b(async_client):
    response = await async_client.get("/errors/resource/999")

    assert response.status_code == 404
    data = response.json()
    assert data["error_code"] == "CUSTOM_B"
    assert data["message"] == "Fake resource not found"


@pytest.mark.asyncio
async def test_validate_user_success(async_client, faker):
    payload = {
        "username": faker.user_name(),
        "age": 25,
        "email": faker.email(),
        "password": "password123",
    }

    response = await async_client.post("/validate-user", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "User data is valid"


@pytest.mark.asyncio
async def test_validate_user_error(async_client):
    payload = {
        "username": "test",
        "age": 15,
        "email": "bad-email",
        "password": "123",
    }

    response = await async_client.post("/validate-user", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert data["error_code"] == "VALIDATION_ERROR"
    assert data["message"] == "Request validation failed"
    assert isinstance(data["details"], list)
