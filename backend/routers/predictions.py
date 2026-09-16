from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema import CropPredictionResponse,CropPredictionRequest
from database.db import get_db

router = APIRouter("/Prediction")

# @router.get("/predict")