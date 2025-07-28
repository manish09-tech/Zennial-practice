from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from database import collection
from schemas import UserRegister, PasswordChangeRequest, ForgotPasswordRequest, ResetPasswordRequest
from auth import (
    hash_password, verify_password, verify_password_policy,
    create_access_token, blacklist_token,
    create_password_reset_token, validate_password_reset_token,
    increment_reset_attempts
)
from security import get_current_user, oauth2_scheme
import logging

router = APIRouter()
logger = logging.getLogger("auth_app")

# Register
@router.post("/register")
async def register_user(user: UserRegister):
    if collection.find_one({"$or": [{"email": user.email}, {"phone": user.phone}]}):
        logger.warning(f"Duplicate registration: {user.email}")
        raise HTTPException(status_code=400, detail="Email or phone already registered")

    try:
        verify_password_policy(user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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
        logger.info(f"User registered: {user.email}")
        return {"message": "User registered successfully"}
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="User already exists")


# Login
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
    logger.info(f"User logged in: {user['email']}")
    return {"access_token": token, "token_type": "bearer"}


# Change Password (auth required)
@router.post("/change-password")
async def change_password(data: PasswordChangeRequest, user=Depends(get_current_user)):
    if not verify_password(data.old_password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect current password")

    try:
        verify_password_policy(data.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    new_hashed = hash_password(data.new_password)
    if new_hashed in user.get("password_history", []):
        raise HTTPException(status_code=400, detail="Cannot reuse old password")

    collection.update_one(
        {"email": user["email"]},
        {"$set": {
            "password": new_hashed,
            "last_password_change": datetime.now()
        },
         "$push": {"password_history": new_hashed}
        }
    )
    logger.info(f"Password changed for user: {user['email']}")
    return {"message": "Password changed successfully. Please log in again."}


# Forgot Password (email token)
@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest):
    user = collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="Email not registered")

    if not increment_reset_attempts(data.email):
        raise HTTPException(status_code=429, detail="Too many reset requests")

    token = create_password_reset_token(data.email)
    logger.info(f"Reset password token sent for: {data.email}")
    return {"reset_token": token, "message": "Reset token created. Use it within 24 hours."}


# Reset Password
@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest):
    email = validate_password_reset_token(data.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    try:
        verify_password_policy(data.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    new_hashed = hash_password(data.new_password)
    user = collection.find_one({"email": email})

    if new_hashed in user.get("password_history", []):
        raise HTTPException(status_code=400, detail="Cannot reuse old password")

    collection.update_one(
        {"email": email},
        {"$set": {"password": new_hashed, "last_password_change": datetime.now()},
         "$push": {"password_history": new_hashed}}
    )
    logger.info(f"Password reset for: {email}")
    return {"message": "Password reset successful. Please log in."}


# Logout (token blacklist)
@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), user=Depends(get_current_user)):
    blacklist_token(token) 
    return {"message": "Logged out successfully"}

