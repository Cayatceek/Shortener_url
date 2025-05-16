from pydantic import BaseModel, HttpUrl

class URLCreate(BaseModel):
    """Схема для создания нового URL."""
    url: HttpUrl

class URLResponse(BaseModel):
    """Схема для ответа с сокращённым URL."""
    short_url: str