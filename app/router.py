from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from .schemas import URLCreate, URLResponse
from .services import create_short_url, get_original_url
import httpx

router = APIRouter()

@router.get("/async-data")
async def fetch_async_data():
    """Выполняет асинхронный запрос к внешнему API.

    Returns:
        dict: Данные, полученные от внешнего API (JSONPlaceholder).

    Raises:
        HTTPException: Код 500, если запрос к внешнему API завершился ошибкой.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://jsonplaceholder.typicode.com/todos/1")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}")
        
@router.post("/", response_model=URLResponse, status_code=201)
async def shorten_url(url: URLCreate):
    """Создаёт сокращённый URL.

    Args:
        url (URLCreate): Объект с оригинальным URL.

    Returns:
        URLResponse: Объект с сокращённым URL.
    """
    short_id = await create_short_url(url.url)
    short_url = f"http://127.0.0.1:8080/{short_id}"
    return URLResponse(short_url=short_url)

@router.get("/{short_id}")
async def redirect_to_original(short_id: str):
    """Перенаправляет на оригинальный URL по сокращённому идентификатору.

    Args:
        short_id (str): Уникальный идентификатор сокращённого URL.

    Returns:
        RedirectResponse: Перенаправление на оригинальный URL с кодом 307.

    Raises:
        HTTPException: Если URL не найден (код 404).
    """
    url_obj = await get_original_url(short_id)
    if url_obj is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=url_obj.original_url, status_code=307)