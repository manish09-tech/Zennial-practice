from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import uuid

from app.database import users_collection
from app.schemas import UserCreate, UserOut
from app.auth import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    existing = await users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(
            status_code=404, detail="Email already registered")
    
    id = str(uuid.uuid4())
    user_doc = {
        "id": id,
        "name": user.name,
        "email": user.email,
        "hashed_password": hash_password(user.password),
        "role": user.role,
        "created_at": datetime.now()
    }

    await users_collection.insert_one(user_doc)

    return UserOut(
        id=id,
        name=user.name,
        email=user.email,
        role=user.role,
        created_at=user_doc["created_at"]
    )