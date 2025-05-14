import aiosqlite
from contextlib import asynccontextmanager

async def init_db():
    """Инициализирует базу данных, создавая таблицу urls, если она не существует."""
    async with aiosqlite.connect("urls.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS urls (short_id TEXT PRIMARY KEY, original_url TEXT)")
        await db.commit()

@asynccontextmanager
async def get_db():
    """Создаёт асинхронное подключение к базе данных SQLite.

    Yields:
        aiosqlite.Connection: Асинхронное соединение с базой данных.
    """
    # Подключаемся к базе данных urls.db
    db = await aiosqlite.connect("urls.db")
    try:
        yield db
    finally:
        # Закрываем соединение
        await db.close()