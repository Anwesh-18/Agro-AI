from fastapi import FastAPI,APIRouter,HTTPException,Depends
from app.schema import LoginRequest,RegisterRequest,CropPredictionRequest,CropPredictionResponse, UserOut
from database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.model import User
from app.utils.jwt_auth import create_access_token,verify_access_token
from pydantic import BaseModel
from app.utils.security import hash_password,verify_password

router = APIRouter(prefix="/auth")
class Token(BaseModel):
    access_token : str
    token_type : str

@router.post("/login",response_model=Token)
async def user_login(user : LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.username == user.username)
    )

    curr_user = result.scalar_one_or_none()

    if not curr_user or not verify_password(user.password, curr_user.password_hash):
        raise HTTPException(status_code=401,detail="Invalid username")

    access_token = create_access_token(data={"sub" : user.username})
    return Token(access_token=access_token,token_type="bearer")

@router.post("/register",response_model=UserOut)
async def register(user : RegisterRequest, db : AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.username == user.username)
    )

    if result.scalar_one_or_none():
        raise HTTPException(status_code=409,detail="User already registered !")

    new_user = User(
        username = user.username,
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        password_hash = hash_password(user.password),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
