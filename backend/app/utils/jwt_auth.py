import os
from datetime import datetime,timedelta,timezone
from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from model import User
from sqlalchemy import select

from dotenv import load_dotenv
from jose import JWTError,jwt

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return token

def verify_access_token(token : str) -> dict:

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={
            "WWW-Authenticate" : "Bearer"
        },
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if not user_id:
            raise credential_exception
        
        return payload
    
    except JWTError:
        raise credential_exception


async def get_current_user(token: str = Depends(oauth2_scheme), db : AsyncSession = Depends(get_db)) -> User:
    payload = verify_access_token(token)

    user_id = payload.get("sub")

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid user ID",
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user not found",
        )

    return user