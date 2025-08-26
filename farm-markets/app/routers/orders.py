from fastapi import APIRouter, Depends, HTTPException, status
from app.database import orders_collection, products_collection, users_collection
from app.auth import get_current_user_id, now_ist_iso
from app.schemas import OrderCreate, OrderOut
from app.utils import new_id

router = APIRouter(prefix="/orders", tags=["Orders"])

# Buyer places an order
@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def place_order(data: OrderCreate, user_id: str = Depends(get_current_user_id)):
    buyer = await users_collection.find_one({"_id": user_id})
    if not buyer or buyer.get("role") != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can place orders")

    product = await products_collection.find_one({"_id": data.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product["quantity"] < data.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    total_price = float(product["price"]) * int(data.quantity)

    order_id = new_id()
    order_doc = {
        "_id": order_id,
        "buyer_id": user_id,
        "farmer_id": product["farmer_id"],
        "product_id": data.product_id,
        "quantity": data.quantity,
        "total_price": total_price,
        "status": "pending",
        "created_at": now_ist_iso(),
    }
    await orders_collection.insert_one(order_doc)

    # decrement stock
    await products_collection.update_one(
        {"_id": data.product_id},
        {"$inc": {"quantity": -data.quantity}}
    )

    return OrderOut(
        id=order_id,
        buyer_id=order_doc["buyer_id"],
        farmer_id=order_doc["farmer_id"],
        product_id=order_doc["product_id"],
        quantity=order_doc["quantity"],
        total_price=order_doc["total_price"],
        status=order_doc["status"],
        created_at=order_doc["created_at"],
    )

# Buyer: my orders
@router.get("/my", response_model=list[OrderOut])
async def my_orders(user_id: str = Depends(get_current_user_id)):
    user = await users_collection.find_one({"_id": user_id})
    if not user or user.get("role") != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can view their orders")

    out: list[OrderOut] = []
    async for o in orders_collection.find({"buyer_id": user_id}):
        out.append(
            OrderOut(
                id=o["_id"],
                buyer_id=o["buyer_id"],
                farmer_id=o["farmer_id"],
                product_id=o["product_id"],
                quantity=o["quantity"],
                total_price=o["total_price"],
                status=o["status"],
                created_at=o.get("created_at", ""),
            )
        )
    return out

# Farmer: incoming orders
@router.get("/incoming", response_model=list[OrderOut])
async def incoming_orders(user_id: str = Depends(get_current_user_id)):
    user = await users_collection.find_one({"_id": user_id})
    if not user or user.get("role") != "farmer":
        raise HTTPException(status_code=403, detail="Only farmers can view incoming orders")

    out: list[OrderOut] = []
    async for o in orders_collection.find({"farmer_id": user_id}):
        out.append(
            OrderOut(
                id=o["_id"],
                buyer_id=o["buyer_id"],
                farmer_id=o["farmer_id"],
                product_id=o["product_id"],
                quantity=o["quantity"],
                total_price=o["total_price"],
                status=o["status"],
                created_at=o.get("created_at", ""),
            )
        )
    return out
