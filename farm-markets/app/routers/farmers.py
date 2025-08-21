from fastapi import APIRouter, Depends, HTTPException
from app.database import farmers_collection, users_collection
from app.auth import get_current_user_id
from app.schemas import UserOut
from bson import ObjectId 

router = APIRouter(prefix="/farmers", tags=["Farmers"])

@router.get("/", response_model=list[UserOut])
async def list_farmers():
    results = []
    cursor = farmers_collection.find()
    async for f in cursor:
        results.append(
            UserOut(
                id=str(f["_id"]),         
                name=f["name"],
                email=f.get("email", ""),
                role="farmer",            
                created_at=f["created_at"]
            )
        )
    return results

@router.get("/me", response_model=UserOut)
async def get_my_farmer_profile(user_id: str = Depends(get_current_user_id)):
    user = await users_collection.find_one({"_id": user_id})
    if not user or user.get("role") != "farmer":
        raise HTTPException(status_code=404, detail="Farmer not found")
    return UserOut(
        id=user["_id"],
        name=user["name"],
        email=user["email"],
        role="farmer",
        created_at=user["created_at"]
    )
