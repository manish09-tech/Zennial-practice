from fastapi import FastAPI, HTTPException
import asyncio
from services import create_customer_account

from models import AddCartRequest, CreateAccountRequest, RemoveCartRequest

app = FastAPI()

@app.post("/create-cus-account")
async def create_cus_account(data: CreateAccountRequest):
    result = await create_customer_account(data.customer_id)
    
    if not result:
        raise HTTPException(status_code=400, detail="Customer already exists")
    return {"message": f"Customer {data.customer_id} created with empty cart "}

@app.post("/add-items")
async def add_to_cart(data: AddCartRequest):
    return True

@app.post("/remove-items")
async def remove_from_cart(data: RemoveCartRequest):
    return True