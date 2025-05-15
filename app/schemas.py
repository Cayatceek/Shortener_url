from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional

class URLCreate(BaseModel):
    """Схема для создания сокращённого URL."""
    url: HttpUrl

    @field_validator("url")
    def validate_url(cls, v):
        """Проверяет, что URL является строкой и валидным HTTP/HTTPS адресом."""
        if not isinstance(v, str):
            raise ValueError("URL must be a string")
        return v

class URLResponse(BaseModel):
    """Схема для ответа с сокращённым URL."""
    short_url: str