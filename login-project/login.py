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

@router.post("/register")
async def register_user(user: UserRegister):
    logging.info(f"Registration attempt: {user.email}")

    if collection.find_one({"email": user.email}):
        logging.warning(f"Email already registered: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")

    verify_password_policy(user.password)
    logging.info(f"Password policy passed: {user.email}")

    hashed_pwd = hash_password(user.password)
    user_dict = user.model_dump()
    user_dict.update({
        "password": hashed_pwd,
        "dob": datetime.combine(user.dob, datetime.min.time()),
        "doj": datetime.combine(user.doj, datetime.min.time()),
        "last_password_change": datetime.now(),
        "password_history": [hashed_pwd],
        "active": True
    })

    try:
        collection.insert_one(user_dict)
        logging.info(f"User registered: {user.email}")
        return {"message": "User registered successfully"}
    except DuplicateKeyError:
        logging.error(f"Duplicate registration: {user.email}")
        raise HTTPException(status_code=400, detail="User already exists")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    logging.info(f"Login attempt: {username}")

    user = collection.find_one({
        "$or": [{"email": username}, {"phone": username}]
    })

    if not user:
        logging.warning(f"Login failed – user not found: {username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user["password"]):
        logging.warning(f"Login failed – incorrect password: {username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    last_change = user.get("last_password_change", user.get("doj"))
    if (datetime.now() - last_change).days > 30:
        logging.info(f"Password expired – force change: {username}")
        raise HTTPException(status_code=403, detail="Password expired. Please change your password.")

    token = create_access_token({"sub": user["email"]})
    logging.info(f"Login successful: {username}")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/change-password")
async def change_password(data: PasswordChangeRequest):
    logging.info(f"Password change attempt: {data.email}")

    user = collection.find_one({"email": data.email})
    if not user:
        logging.warning(f"Password change – user not found: {data.email}")
        raise HTTPException(status_code=401, detail="Incorrect current password")

    if not verify_password(data.old_password, user["password"]):
        logging.warning(f"Password change – incorrect old password: {data.email}")
        raise HTTPException(status_code=401, detail="Incorrect current password")

    verify_password_policy(data.new_password)
    if is_password_reused(data.new_password, user.get("password_history", [])):
        logging.warning(f"Password reuse attempt: {data.email}")
        raise HTTPException(status_code=400, detail="Cannot reuse old password")

    new_hashed = hash_password(data.new_password)
    update_password(data.email, new_hashed)
    logging.info(f"Password changed: {data.email}")
    raise HTTPException(status_code=200, detail="Password changed. Please log in again.")

@router.post("/logout")
async def logout():
    logging.info("User logged out successfully.")
    return {"message": "User logged out successfully."}
