import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from app.database import blacklisted_tokens_collection

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Only used to parse the Bearer token from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Hash & verify
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# IST helper
IST = timezone(timedelta(hours=5, minutes=30))
def now_ist_iso() -> str:
    return datetime.now(IST).isoformat()

# JWT creation
def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# JWT decoding -> returns user_id (string)
async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    # check blacklist
    if await is_token_blacklisted(token):
        raise HTTPException(status_code=401, detail="Token has been logged out")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    
async def is_token_blacklisted(token: str):
    doc = await blacklisted_tokens_collection.find_one({"token": token})
    return doc is not None
