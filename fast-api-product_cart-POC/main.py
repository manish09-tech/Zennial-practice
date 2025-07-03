from fastapi import FastAPI, HTTPException
import asyncio
from services import add_cart, create_customer_account, remove_product

from models import AddCartRequest, CreateAccountRequest, RemoveCartRequest

app = FastAPI()

@app.post("/create-cus-account")
async def create_cus_account(data: CreateAccountRequest):
    result = await create_customer_account(data.customer_id)
    
    if not result:
        raise HTTPException(status_code=400, detail="The following customer ID is already exists.")
    return {"message": f"A customer with ID {data.customer_id} has been created."}

@app.post("/add-items")
async def add_to_cart(data: AddCartRequest):
    products = await add_cart(data.customer_id, data.product)
    return {"message" : f"Customer with ID: {data.customer_id} added {data.product} items to their cart. The cart now contains {products} available items."}

@app.post("/remove-items")
async def remove_from_cart(data: RemoveCartRequest):
    try:
        products = await remove_product(data.customer_id, data.product)
        return {"message" : f"Removed {data.product} items from customer ID {data.customer_id}. {products} items remain in the cart."}
    except ValueError as e:
        raise HTTPException (status_code=400, detail= str(e))
    except Exception as e:
        raise HTTPException (status_code=400, detail= str(e))
