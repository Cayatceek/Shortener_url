import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_shorten_url():
    """Тестирует создание сокращённого URL.

    Проверяет, что запрос POST / возвращает код 201 и содержит сокращённый URL.
    """
    response = client.post("/", json={"url": "http://example.com"})
    assert response.status_code == 201
    assert "short_url" in response.json()

@pytest.mark.asyncio
async def test_redirect_url():
    """Тестирует перенаправление на оригинальный URL.

    Проверяет, что запрос GET /<short_id> возвращает код 307 и правильный заголовок Location.
    """
    response = client.post("/", json={"url": "http://example.com"})
    short_url = response.json()["short_url"]
    short_id = short_url.split("/")[-1]
    
    response = client.get(f"/{short_id}", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "http://example.com"

@pytest.mark.asyncio
async def test_async_data():
    """Тестирует асинхронный запрос к внешнему API.

    Проверяет, что запрос GET /async-data возвращает код 200 и содержит данные.
    """
    response = client.get("/async-data")
    assert response.status_code == 200
    assert "id" in response.json()