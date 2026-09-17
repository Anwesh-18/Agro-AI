from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema import CropPredictionResponse,CropPredictionRequest
from database.db import get_db
from app.utils.jwt_auth import get_current_user
from app.model import User,Prediction

router = APIRouter(prefix="/Prediction",tags=["predictions"])

# @router.post("/",response_model=CropPredictionResponse)
# async def predict_crop(data: CropPredictionRequest, db : AsyncSession = Depends(get_db), current_user : User = Depends(get_current_user)):
