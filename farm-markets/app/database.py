import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# load environment
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "farm_markets_db")

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB]

users_collection = db.get_collection("users")
farmers_collection = db.get_collection("farmers")
products_collection = db.get_collection("products")
orders_collection = db.get_collection("orders")
buyers_collection = db.get_collection("buyers")
