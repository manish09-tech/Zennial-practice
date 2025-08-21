# app/routers/users.py
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import uuid

from app.database import users_collection, farmers_collection
from app.schemas import UserCreate, UserOut, LoginData, Token
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    existing = await users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    id = str(uuid.uuid4())
    user_doc = {
        "id": id,
        "name": user.name,
        "email": user.email,
        "hashed_password": hash_password(user.password),
        "role": user.role,
        "created_at": datetime.utcnow()
    }

    await users_collection.insert_one(user_doc)

    # If farmer, add to farmers_collection 
    if user.role == "farmer":
        farmer_doc = {
            "id": id,
            "name": user.name,
            "email": user.email,
            "created_at": user_doc["created_at"]
        }
        await farmers_collection.update_one({"id": id}, {"$set": farmer_doc}, upsert=True)

    return UserOut(**user_doc)

@router.post("/login", response_model=Token)
async def login(data: LoginData):
    user = await users_collection.find_one({"email": data.email})
    if not user or not verify_password(data.password, user.get("hashed_password", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(user["_id"])
    return {"access_token": token, "token_type": "bearer"}
