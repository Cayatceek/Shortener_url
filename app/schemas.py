from pydantic import BaseModel

class URLCreate(BaseModel):
    """Схема для создания нового URL.

    Attributes:
        url (str): Оригинальный URL для сокращения.
    """
    url: str

class URLResponse(BaseModel):
    """Схема для ответа с сокращённым URL.

    Attributes:
        short_url (str): Сокращённый URL.
    """
    short_url: str