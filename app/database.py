import aiosqlite
from contextlib import asynccontextmanager
from abc import ABC, abstractmethod
from typing import Any, Optional
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Base(ABC):
    @classmethod
    @abstractmethod
    async def create(cls, db: aiosqlite.Connection, **kwargs) -> None:
        pass
    
    @classmethod
    @abstractmethod
    async def get_by_id(cls, db: aiosqlite.Connection, id: str) -> Optional[Any]:
        pass

# Явный путь к базе данных
DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "urls.db"))


async def init_db():
    """Инициализирует базу данных."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS urls (short_id TEXT PRIMARY KEY, original_url TEXT)")
        await db.commit()

@asynccontextmanager
async def get_db():
    """Создаёт асинхронное подключение к базе данных."""
    db = await aiosqlite.connect(DB_PATH)
    yield db
    await db.close()