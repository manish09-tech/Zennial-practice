import asyncio
from db import accounts

async def create_customer_account(customer_id: str):
    if customer_id in accounts:
        return False 
    accounts[customer_id] = 0
    return True

