import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# load environment
load_dotenv()

MONGO_URL = os.getenv("MONGO_URI")
if not MONGO_URL:
    raise RuntimeError("MONGO_URI not set in environment or .env")

client = AsyncIOMotorClient(MONGO_URL)
db = client["farm_markets_db"]

users_collection = db.get_collection("users")
farmers_collection = db.get_collection("farmers")
products_collection = db.get_collection("products")
orders_collection = db.get_collection("orders")
