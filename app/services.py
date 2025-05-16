import secrets
from .curd import save_url, get_url_by_short_id
from .models import URL
from pydantic import HttpUrl
from typing import Optional

class URLService:
    """Сервис для операций с сокращением URL."""

    @staticmethod
    def generate_short_id() -> str:
        """Генерирует короткий идентификатор для URL с использованием secrets."""
        return secrets.token_urlsafe(6)

    async def create_short_url(self, original_url: HttpUrl) -> str:
        """Создаёт сокращённый URL."""
        url_str = str(original_url)
        if not url_str.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL: must start with http:// or https://")
        short_id = self.generate_short_id()
        await save_url(short_id, url_str)
        return short_id

    async def get_original_url(self, short_id: str) -> Optional[URL]:
        """Получает оригинальный URL по короткому идентификатору."""
        return await get_url_by_short_id(short_id)