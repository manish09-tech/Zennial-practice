from pymongo import MongoClient

#connet to MongoDB
client = MongoClient("mongodb+srv://manishsaijakkula:Manishj09@news-article.jjyhq8r.mongodb.net/")
database = client["user_db"]
collection = database["users"]