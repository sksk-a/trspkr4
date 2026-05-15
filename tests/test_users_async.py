import pytest


@pytest.mark.asyncio
async def test_create_user_201(async_client, faker):
    payload = {"username": faker.user_name(), "age": faker.random_int(min=19, max=60)}

    response = await async_client.post("/users", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == payload["username"]
    assert data["age"] == payload["age"]


@pytest.mark.asyncio
async def test_get_existing_user_200(async_client, faker):
    payload = {"username": faker.user_name(), "age": faker.random_int(min=19, max=60)}
    create_response = await async_client.post("/users", json=payload)
    user_id = create_response.json()["id"]

    response = await async_client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json() == {"id": user_id, **payload}


@pytest.mark.asyncio
async def test_get_missing_user_404(async_client):
    response = await async_client.get("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_delete_existing_user_204(async_client, faker):
    payload = {"username": faker.user_name(), "age": faker.random_int(min=19, max=60)}
    create_response = await async_client.post("/users", json=payload)
    user_id = create_response.json()["id"]

    response = await async_client.delete(f"/users/{user_id}")

    assert response.status_code == 204
    assert response.text == ""


@pytest.mark.asyncio
async def test_delete_same_user_twice_404(async_client, faker):
    payload = {"username": faker.user_name(), "age": faker.random_int(min=19, max=60)}
    create_response = await async_client.post("/users", json=payload)
    user_id = create_response.json()["id"]

    first_response = await async_client.delete(f"/users/{user_id}")
    second_response = await async_client.delete(f"/users/{user_id}")

    assert first_response.status_code == 204
    assert second_response.status_code == 404
    assert second_response.json()["detail"] == "User not found"
