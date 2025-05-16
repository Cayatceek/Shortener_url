from dataclasses import dataclass
from .database import Base
import aiosqlite
from typing import Optional

@dataclass
class URL(Base):
    """Модель данных для URL."""
    short_id: str
    original_url: str

    @classmethod
    async def create(cls, db: aiosqlite.Connection, **kwargs) -> None:
        """Создаёт запись в базе данных."""
        short_id = kwargs.get("short_id")
        original_url = kwargs.get("original_url")
        await db.execute(
            "INSERT INTO urls (short_id, original_url) VALUES (?, ?)",
            (short_id, original_url)
        )
        await db.commit()

    @classmethod
    async def get_by_id(cls, db: aiosqlite.Connection, id: str) -> Optional['URL']:
        """Получает запись из базы данных по short_id."""
        cursor = await db.execute(
            "SELECT short_id, original_url FROM urls WHERE short_id = ?", (id,)
        )
        row = await cursor.fetchone()
        return cls(short_id=row[0], original_url=row[1]) if row else None