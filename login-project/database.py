from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["user_db"]

collection = db["users"]
token_blacklist = db["blacklisted_tokens"]
reset_tokens = db["reset_tokens"]








