"""Модуль для работы с базой данных SQLite. 🔌"""

import aiosqlite
from contextlib import asynccontextmanager

async def init_db():
    """Инициализирует базу данных, создавая таблицу urls, если она не существует."""
    async with aiosqlite.connect("/app/urls.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS urls (short_id TEXT PRIMARY KEY, original_url TEXT)")
        await db.commit()

@asynccontextmanager
async def get_db():
    """Создаёт асинхронное подключение к базе данных SQLite.

    Yields:
        aiosqlite.Connection: Асинхронное соединение с базой данных.
    """
    db = await aiosqlite.connect("/app/urls.db")
    try:
        yield db
    finally:
        await db.close()