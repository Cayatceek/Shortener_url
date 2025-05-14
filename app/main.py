from fastapi import FastAPI
from .router import router
from .database import init_db
import asyncio

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Инициализирует базу данных при старте приложения."""
    await init_db()