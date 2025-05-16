from fastapi import FastAPI
from .router import router
from .database import init_db

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    await init_db()