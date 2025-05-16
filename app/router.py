from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from .schemas import URLCreate, URLResponse
from .services import URLService
import httpx


router = APIRouter()
url_service = URLService()

@router.get("/async-data")
async def fetch_async_data():
    """Выполняет асинхронный запрос к внешнему API."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/todos/1")
        response.raise_for_status()
        return response.json()


@router.post("/", response_model=URLResponse, status_code=201)
async def shorten_url(url: URLCreate, request: Request):
    """Создаёт сокращённый URL."""
    short_id = await url_service.create_short_url(url.url)
    return URLResponse(short_url=f"http://127.0.0.1:8080/{short_id}")

@router.get("/{short_id}")
async def redirect_to_original(short_id: str):
    """Перенаправляет на оригинальный URL по сокращённому идентификатору."""
    url_obj = await url_service.get_original_url(short_id)
    if url_obj is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=url_obj.original_url, status_code=307)
    