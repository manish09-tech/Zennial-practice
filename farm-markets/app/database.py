import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://manishsaijakkula:Manishj09@news-article.jjyhq8r.mongodb.net/")
MONGO_DB = os.getenv("MONGO_DB", "farm_markets_db")

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB]

users_collection = db.get_collection("users")
farmers_collection = db.get_collection("farmers")
products_collection = db.get_collection("products")
orders_collection = db.get_collection("orders")
buyers_collection = db.get_collection("buyers")
blacklisted_tokens_collection = db.get_collection("blacklisted_tokens")

# TTL(time-to-live) index for blacklisted tokens
async def init_indexes():
    # automatically delete expired tokens
    await blacklisted_tokens_collection.create_index(
        "expires_at", expireAfterSeconds=0
    )

