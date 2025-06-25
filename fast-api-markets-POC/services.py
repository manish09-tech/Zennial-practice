import asyncio
from db import accounts

async def create_customer_account(customer_id: str):
    if customer_id in accounts:
        return False 
    accounts[customer_id] = 0
    return True

async def add_cart(customer_id: str, product: int):
    if customer_id not in accounts:
        raise ValueError(f"Account does not exists for customer with id: {customer_id}")
    accounts[customer_id] += product
    return accounts[customer_id]