from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.database import products_collection, users_collection
from app.auth import get_current_user_id, now_ist_iso
from app.schemas import ProductCreate, ProductUpdate, ProductOut
from app.utils import new_id

router = APIRouter(prefix="/products", tags=["Products"])

# Create Product (Farmer only)
@router.post("/", response_model=ProductOut, status_code=201)
async def create_product(data: ProductCreate, user_id: str = Depends(get_current_user_id)):
    user = await users_collection.find_one({"_id": user_id})
    if not user or user.get("role") != "farmer":
        raise HTTPException(status_code=403, detail="Only farmers can create products")

    _id = new_id()  # using string-based IDs consistently
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
    return ProductOut(**{
        "id": _id,
        "name": doc["name"],
        "description": doc.get("description"),
        "price": doc["price"],
        "quantity": doc["quantity"],
        "farmer_id": doc["farmer_id"],
        "created_at": doc["created_at"],
    })

# List Products (Anyone)
@router.get("/", response_model=list[ProductOut])
async def list_products():
    items: list[ProductOut] = []
    async for p in products_collection.find():
        items.append(ProductOut(**{
            "id": p["_id"],
            "name": p["name"],
            "description": p.get("description"),
            "price": p["price"],
            "quantity": p["quantity"],
            "farmer_id": p["farmer_id"],
            "created_at": p.get("created_at", ""),
        }))
    return items

# Verify Farmer
async def verify_farmer(user_id: str):
    user = await users_collection.find_one({"_id": user_id})
    if not user or user.get("role") != "farmer":
        raise HTTPException(status_code=403, detail="Only farmers can perform this action")
    return user

# Update Product (Farmer only, own products)
@router.put("/{product_id}", response_model=ProductOut)
async def update_product(product_id: str, product: ProductUpdate, user_id: str = Depends(get_current_user_id)):
    await verify_farmer(user_id)

    existing = await products_collection.find_one({"_id": product_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")

    if existing["farmer_id"] != user_id:
        raise HTTPException(status_code=403, detail="You can update only your own products")

    update_data = {k: v for k, v in product.dict().items() if v is not None}
    await products_collection.update_one({"_id": product_id}, {"$set": update_data})

    updated = await products_collection.find_one({"_id": product_id})
    return ProductOut(**{
        "id": updated["_id"],
        "name": updated["name"],
        "description": updated.get("description"),
        "price": updated["price"],
        "quantity": updated["quantity"],
        "farmer_id": updated["farmer_id"],
        "created_at": updated.get("created_at", ""),
    })

# Delete Product (Farmer only, own products)
@router.delete("/{product_id}")
async def delete_product(product_id: str, user_id: str = Depends(get_current_user_id)):
    await verify_farmer(user_id)

    existing = await products_collection.find_one({"_id": product_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")

    if existing["farmer_id"] != user_id:
        raise HTTPException(status_code=403, detail="You can delete only your own products")

    await products_collection.delete_one({"_id": product_id})
    return {"message": "Product deleted successfully"}
