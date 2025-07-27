from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

#connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://manishsaijakkula:Manishj09@news-article.jjyhq8r.mongodb.net/")
client = MongoClient(MONGO_URI)
database = client["user_db"]
collection = database["users"]








