from fastapi import FastAPI,APIRouter,HTTPException,Depends
from backend.app.schema import LoginRequest,RegisterRequest,CropPredictionRequest,CropPredictionResponse
from backend.database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.model import User
from app.utils.jwt_auth import create_access_token,verify_access_token

router = APIRouter(prefix=["/auth"])

@router.get("/login")
async def user_login(user : LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.username == user.username)
    )

    curr_user = result.scalar_one_or_none()

    if not curr_user:
        raise HTTPException(status_code=401,detail="Invalid username")
