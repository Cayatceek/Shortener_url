from dataclasses import dataclass

@dataclass
class URL:
    """Модель данных для URL.

    Attributes:
        short_id (str): Уникальный идентификатор сокращённого URL.
        original_url (str): Оригинальный URL.
    """
    short_id: str
    original_url: str