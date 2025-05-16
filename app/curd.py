from typing import Optional
from .models import URL
from .database import get_db

async def save_url(short_id: str, original_url: str):
    """Создаёт запись в базе данных с short_id и original_url."""
    async with get_db() as db:
        await URL.create(db, short_id=short_id, original_url=original_url)

async def get_url_by_short_id(short_id: str) -> Optional[URL]:
    """Получает запись из базы данных по short_id."""
    async with get_db() as db:
        return await URL.get_by_id(db, short_id)