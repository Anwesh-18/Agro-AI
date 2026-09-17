from fastapi import FastAPI
from routers.auth import router as auth_router
from app.model import Base
from database.db import engine
# from routers.predictions import router as pred_router


app = FastAPI()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup():
    await create_tables()

app.include_router(auth_router)
# app.include_router(pred_router)