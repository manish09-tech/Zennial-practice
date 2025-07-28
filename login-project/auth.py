from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os, re
from database import token_blacklist, reset_tokens
import logging

load_dotenv()
logger = logging.getLogger("auth_app")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# JWT Functions
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


# Password Hashing
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)


# Password Policy
def verify_password_policy(password: str):
    if not (8 <= len(password) <= 20):
        raise ValueError("Password must be 8-20 characters")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Must contain uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValueError("Must contain lowercase letter")
    if not re.search(r"[0-9]", password):
        raise ValueError("Must contain a digit")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Must contain a special character")


# Token Blacklist
def blacklist_token(token: str):
    if not isinstance(token, str):
        raise ValueError("Invalid token type")
    token_blacklist.insert_one({"token": token})

def is_token_blacklisted(token: str) -> bool:
    return token_blacklist.find_one({"token": token}) is not None


# Forgot Password Token
def create_password_reset_token(email: str):
    token = create_access_token({"sub": email}, timedelta(hours=24))
    reset_tokens.insert_one({
        "email": email,
        "token": token,
        "created_at": datetime.now(),
        "attempts": 1
    })
    logger.info(f"Reset token created for {email}")
    return token

def validate_password_reset_token(token: str):
    record = reset_tokens.find_one({"token": token})
    if not record:
        return None
    age = (datetime.now() - record["created_at"]).total_seconds()
    if age > 86400:  # 24 hrs
        return None
    return record["email"]

def increment_reset_attempts(email: str):
    record = reset_tokens.find_one({"email": email})
    if record and record.get("attempts", 0) >= 3:
        return False
    reset_tokens.update_one({"email": email}, {"$inc": {"attempts": 1}}, upsert=True)
    return True
