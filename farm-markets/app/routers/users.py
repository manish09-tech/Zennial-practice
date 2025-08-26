from fastapi import APIRouter, HTTPException, status, Depends
from app.database import users_collection, farmers_collection, buyers_collection
from app.schemas import UserCreate, UserOut, LoginData, Token
from app.auth import hash_password, verify_password, create_access_token, now_ist_iso, get_current_user_id
from app.utils import new_id

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserOut, status_code=201)
async def register(user: UserCreate):
    existing = await users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    _id = new_id()
    user_doc = {
        "_id": _id,  # store as string
        "name": user.name,
        "email": user.email,
        "hashed_password": hash_password(user.password),
        "role": user.role,
        "created_at": now_ist_iso(),
    }
    await users_collection.insert_one(user_doc)

    # If farmer, mirror minimal profile into farmers collection
    if user.role == "farmer":
        farmer_doc = {
            "_id": _id,
            "name": user.name,
            "email": user.email,
            "role": "farmer",
            "created_at": user_doc["created_at"],
        }
        await farmers_collection.update_one(
            {"_id": _id}, {"$set": farmer_doc}, upsert=True
        )

    # If buyer, mirror minimal profile into buyers collection
    if user.role == "buyer":
        buyer_doc = {
            "_id": _id,
            "name": user.name,
            "email": user.email,
            "role": "buyer",
            "created_at": user_doc["created_at"],
        }
        await buyers_collection.update_one(
            {"_id": _id}, {"$set": buyer_doc}, upsert=True
        )

    return UserOut(
        id=_id,
        name=user_doc["name"],
        email=user_doc["email"],
        role=user_doc["role"],
        created_at=user_doc["created_at"],
    )


@router.post("/login", response_model=Token)
async def login(data: LoginData):
    user = await users_collection.find_one({"email": data.email})
    if not user or not verify_password(data.password, user.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token(user["_id"])
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
async def me(user_id: str = Depends(get_current_user_id)):
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(
        id=user["_id"],
        name=user.get("name", ""),
        email=user["email"],
        role=user.get("role", ""),
        created_at=user.get("created_at", ""),
    )
