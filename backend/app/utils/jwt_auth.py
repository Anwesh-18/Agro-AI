import os
from datetime import datetime,timedelta,timezone
from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv
from jose import JWTError,jwt

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

if not SECRET_KEY:
    raise "SECRET_KEY not set"

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=[ALGORITHM],
    )

    return token

def verify_access_token(token : str) -> bool:

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={
            "www-Aunthenticate" : "Bearer"
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