from fastapi import APIRouter, Depends, HTTPException
from app.database import products_collection, users_collection
from app.auth import get_current_user_id, now_ist_iso
from app.schemas import ProductCreate, ProductOut
from app.utils import new_id

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductOut, status_code=201)
async def create_product(data: ProductCreate, user_id: str = Depends(get_current_user_id)):
    # only farmers
    user = await users_collection.find_one({"_id": user_id})
    if not user or user.get("role") != "farmer":
        raise HTTPException(status_code=403, detail="Only farmers can create products")

    _id = new_id()
    doc = {
        "_id": _id,
        "farmer_id": user_id,
        "name": data.name,
        "description": data.description,
        "price": data.price,
        "quantity": data.quantity,
        "created_at": now_ist_iso(),
    }
    await products_collection.insert_one(doc)
    return ProductOut(
        id=_id,
        name=doc["name"],
        description=doc.get("description"),
        price=doc["price"],
        quantity=doc["quantity"],
        farmer_id=doc["farmer_id"],
        created_at=doc["created_at"],
    )

@router.get("/", response_model=list[ProductOut])
async def list_products():
    items: list[ProductOut] = []
    async for p in products_collection.find():
        items.append(
            ProductOut(
                id=p["_id"],
                name=p["name"],
                description=p.get("description"),
                price=p["price"],
                quantity=p["quantity"],
                farmer_id=p["farmer_id"],
                created_at=p.get("created_at", ""),
            )
        )
    return items
