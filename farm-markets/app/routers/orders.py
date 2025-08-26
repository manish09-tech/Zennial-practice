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

    return OrderOut(**order_doc, id=order_id)


# Buyer updates own order (only if pending)
@router.put("/{order_id}", response_model=OrderOut)
async def update_order(order_id: str, data: OrderCreate, user_id: str = Depends(get_current_user_id)):
    buyer = await users_collection.find_one({"_id": user_id})
    if not buyer or buyer.get("role") != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can update orders")

    order = await orders_collection.find_one({"_id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order["buyer_id"] != user_id:
        raise HTTPException(status_code=403, detail="You can update only your own orders")

    if order["status"] != "pending":
        raise HTTPException(status_code=400, detail="Only pending orders can be updated")

    product = await products_collection.find_one({"_id": order["product_id"]})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # restore previous stock before checking new quantity
    await products_collection.update_one(
        {"_id": order["product_id"]},
        {"$inc": {"quantity": order["quantity"]}}
    )

    if product["quantity"] + order["quantity"] < data.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    total_price = float(product["price"]) * int(data.quantity)

    await orders_collection.update_one(
        {"_id": order_id},
        {"$set": {"quantity": data.quantity, "total_price": total_price}}
    )

    # decrement stock again
    await products_collection.update_one(
        {"_id": order["product_id"]},
        {"$inc": {"quantity": -data.quantity}}
    )

    updated = await orders_collection.find_one({"_id": order_id})
    return OrderOut(**updated, id=updated["_id"])


# Buyer deletes own order (restore stock if pending)
@router.delete("/{order_id}")
async def delete_order(order_id: str, user_id: str = Depends(get_current_user_id)):
    buyer = await users_collection.find_one({"_id": user_id})
    if not buyer or buyer.get("role") != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can delete orders")

    order = await orders_collection.find_one({"_id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order["buyer_id"] != user_id:
        raise HTTPException(status_code=403, detail="You can delete only your own orders")

    if order["status"] != "pending":
        raise HTTPException(status_code=400, detail="Only pending orders can be deleted")

    # restore stock
    await products_collection.update_one(
        {"_id": order["product_id"]},
        {"$inc": {"quantity": order["quantity"]}}
    )

    await orders_collection.delete_one({"_id": order_id})
    return {"message": "Order deleted successfully"}
