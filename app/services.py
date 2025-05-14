import secrets
from .database import get_db
from .models import URL

async def create_short_url(original_url: str) -> str:
    """Создаёт запись с сокращённым URL в базе данных.

    Args:
        original_url (str): Оригинальный URL для сокращения.

    Returns:
        str: Уникальный идентификатор сокращённого URL.
    """
    short_id = secrets.token_urlsafe(6)
    async with get_db() as db:
        await db.execute("CREATE TABLE IF NOT EXISTS urls (short_id TEXT PRIMARY KEY, original_url TEXT)")
        await db.execute("INSERT INTO urls (short_id, original_url) VALUES (?, ?)", (short_id, original_url))
        await db.commit()
    return short_id

async def get_original_url(short_id: str) -> URL:
    """Получает URL по его сокращённому идентификатору.

    Args:
        short_id (str): Уникальный идентификатор сокращённого URL.

    Returns:
        URL: Объект модели URL с данными о сокращённом и оригинальном URL,
             или None, если URL не найден.
    """
    async with get_db() as db:
        result = await db.execute("SELECT short_id, original_url FROM urls WHERE short_id = ?", (short_id,))
        row = await result.fetchone()
        return URL(short_id=row[0], original_url=row[1]) if row else None