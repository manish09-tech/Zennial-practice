from fastapi import APIRouter, Depends, HTTPException
from app.database import users_collection, buyers_collection
from app.auth import get_current_user_id
from app.schemas import UserOut

router = APIRouter(prefix="/buyers", tags=["Buyers"])

@router.get("/", response_model=list[UserOut])
async def list_farmers():
    results: list[UserOut] = []
    async for b in buyers_collection.find():
        results.append(
            UserOut(
                id=b["_id"],
                name=b.get("name", ""),
                email=b.get("email", ""),
                role=b.get("role", "farmer"),
                created_at=b.get("created_at", ""),
            )
        )
    return results

@router.get("/me", response_model=UserOut)
async def my_buyer_profile(user_id: str = Depends(get_current_user_id)):
    user = await users_collection.find_one({"_id": user_id})
    if not user or user.get("role") != "buyer":
        raise HTTPException(status_code=404, detail="Buyer not found")
    return UserOut(
        id=user["_id"],
        name=user.get("name", ""),
        email=user["email"],
        role=user["role"],
        created_at=user.get("created_at", ""),
    )


