from pymongo import MongoClient

# MongoDB setup
mongo_cluster = "mongodb+srv://manishsaijakkula:Manishj09@news-article.jjyhq8r.mongodb.net/"

client = MongoClient(mongo_cluster)
database_name = "practise_db"
collection = "employees"

database = client[database_name]
employee_collection = database[collection]

# employee_collection.insert_many([
#     {"name" : "Rahul", "city" : "HYD", "salary" : 25000, "address" : {"street": "filmnagar", "pin_code" : 500039}},
#     {"name" : "Umesh", "city" : "HYD", "salary" : 30000, "address" : {"street": "bandra", "pin_code" : 500045}},
#     {"name" : "Roopesh", "city" : "HYD", "salary" : 55000, "address" : {"street": "filmnagar", "pin_code" : 500039}}
# ])

employee_collection.delete_many({
    "address.pin_code" : {"$lt" : 500045}
})

print ("Done!!")





