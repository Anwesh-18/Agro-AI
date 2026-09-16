from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.predictions import router as pred_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(pred_router)