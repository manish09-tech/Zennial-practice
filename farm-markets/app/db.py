import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://manishsaijakkula:Manishj09@news-article.jjyhq8r.mongodb.net/")
client = AsyncIOMotorClient(MONGO_URL)
db = client["farm_markets_db"]

users_collection = db.get_collection("users")
products_collection = db.get_collection("products")
orders_collection = db.get_collection("orders")