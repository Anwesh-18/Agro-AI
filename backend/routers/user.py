from fastapi import FastAPI,HTTPException,Depends,APIRouter
from app.utils.jwt_auth import get_current_user
from app.model import User


router = APIRouter("/users")


@router.get("/me")
async def get_me(current_user : User = Depends(get_current_user)):
    return current_user