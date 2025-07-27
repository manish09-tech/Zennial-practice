from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from database import collection
from auth import (
    hash_password, verify_password, verify_password_policy,
    create_access_token
)
from datetime import datetime
from models import is_password_reused, update_password
from schemas import UserRegister, PasswordChangeRequest
from pymongo.errors import DuplicateKeyError
import logging

router = APIRouter()

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("user.log"),
        logging.StreamHandler()
    ]
)

@router.post("/register")
async def register_user(user: UserRegister):
    if collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    verify_password_policy(user.password)

    hashed_pwd = hash_password(user.password)
    user_dict = user.model_dump()
    user_dict.update({
        "password": hashed_pwd,
        "dob": datetime.combine(user.dob, datetime.min.time()),
        "doj": datetime.combine(user.doj, datetime.min.time()),
        "last_password_change": datetime.utcnow(),
        "password_history": [hashed_pwd],
        "active": True
    })

    try:
        collection.insert_one(user_dict)
        return {"message": "User registered successfully"}
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="User already exists")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    user = collection.find_one({
        "$or": [{"email": username}, {"phone": username}]
    })

    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    last_change = user.get("last_password_change", user.get("doj"))
    if (datetime.now() - last_change).days > 30:
        raise HTTPException(status_code=403, detail="Password expired. Please change your password.")

    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/change-password")
async def change_password(data: PasswordChangeRequest):
    user = collection.find_one({"email": data.email})
    
    if not user or not verify_password(data.old_password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect current password")

    verify_password_policy(data.new_password)

    if is_password_reused(data.new_password, user.get("password_history", [])):
        raise HTTPException(status_code=400, detail="Cannot reuse old password")

    new_hashed = hash_password(data.new_password)
    update_password(data.email, new_hashed)

    raise HTTPException(status_code=200, detail="Password changed. Please log in again.")

@router.post("/logout")
async def logout():
    return {"message": "User logged out successfully."}
