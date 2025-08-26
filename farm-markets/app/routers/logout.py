from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt, JWTError
from app.auth import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.database import blacklisted_tokens_collection
from datetime import datetime

router = APIRouter(prefix="/users", tags=["Users"])

# check token expiry from JWT
def get_token_expiry(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return datetime.fromtimestamp(payload.get("exp"))
    except JWTError:
        return None

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    expiry = get_token_expiry(token)
    if not expiry:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check if already blacklisted
    existing = await blacklisted_tokens_collection.find_one({"token": token})
    if existing:
        raise HTTPException(status_code=400, detail="Token already invalidated")

    # Store in blacklist
    await blacklisted_tokens_collection.insert_one({
        "token": token,
        "expires_at": expiry
    })

    return {"message": "Logout successful"}
