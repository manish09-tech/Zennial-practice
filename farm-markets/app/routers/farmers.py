from fastapi import APIRouter, Depends, HTTPException
from app.database import farmers_collection, users_collection
from app.auth import get_current_user_id
from app.schemas import UserOut

router = APIRouter(prefix="/farmers", tags=["Farmers"])

@router.get("/", response_model=list[UserOut])
async def list_farmers():
    results: list[UserOut] = []
    async for f in farmers_collection.find():
        results.append(
            UserOut(
                id=f["_id"],
                name=f.get("name", ""),
                email=f.get("email", ""),
                role=f.get("role", "farmer"),
                created_at=f.get("created_at", ""),
            )
        )
    return results

@router.get("/me", response_model=UserOut)
async def my_farmer_profile(user_id: str = Depends(get_current_user_id)):
    user = await users_collection.find_one({"_id": user_id})
    if not user or user.get("role") != "farmer":
        raise HTTPException(status_code=404, detail="Farmer not found")
    return UserOut(
        id=user["_id"],
        name=user.get("name", ""),
        email=user["email"],
        role=user["role"],
        created_at=user.get("created_at", ""),
    )
