
# PyMongo vs Motor in FastAPI

## PyMongo (Synchronous – Blocking)

PyMongo is the official synchronous Python driver for MongoDB. It provides a standard, blocking interface for interacting with MongoDB databases. This means that when a PyMongo operation (like a query or an insert) is executed, the program execution pauses until the database operation completes. This is suitable for applications where blocking I/O does not significantly impact performance or responsiveness.

### Example
```python
from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()

client = MongoClient("mongodb+srv://manishsaijakkula:*******@news-article.jjyhq8r.mongodb.net/")
db = client["pymongodb"]
collection = db["users"]

class User(BaseModel):
    name: str
    email: str

@app.post("/add_user")
def add_user(user: User):
    collection.insert_one(user.dict())
    return {"status": "User added"}

@app.get("/get_user/{name}")
def get_user(name: str):
    user = collection.find_one({"name": name})
    if user:
        user["_id"] = str(user["_id"])
    return user
```

### Sample Output

```json
POST /add_user
{
    "status": "User added"
}

GET /get_user/manish
{
    "_id": "64f688f0b435ae9a16fdbfcb",
    "name": "manish",
    "email": "manish@gmail.com"
}
```

---

## Motor (Asynchronous)

Motor was an asynchronous Python driver for MongoDB, designed for use with asynchronous frameworks like Tornado and asyncio. It provided a non-blocking interface, allowing database operations to be performed concurrently without pausing the entire application. This was particularly beneficial for applications requiring high concurrency, such as web servers or real-time applications.


### Example
```python
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

app = FastAPI()

client = AsyncIOMotorClient("mongodb+srv://manishsaijakkula:*******@news-article.jjyhq8r.mongodb.net/")
db = client["motordb"]
collection = db["users"]

class User(BaseModel):
    name: str
    email: str

@app.post("/add_user")
async def add_user(user: User):
    result = await collection.insert_one(user.dict())
    return {"inserted_id": str(result.inserted_id)}

@app.get("/get_user/{name}")
async def get_user(name: str):
    user = await collection.find_one({"name": name})
    if user:
        user["_id"] = str(user["_id"])
    return user
```

### Sample Output

```json
POST /add_user
{
    "inserted_id": "64f688f0b435ae9a16fdbfc9"
}

GET /get_user/Ameet
{
    "_id": "64f688f0b435ae9a16fdbfc9",
    "name": "Ameet",
    "email": "ameet@gmail.com"
}
```

---

## Summary

| Feature               | PyMongo                      | Motor                          |
|-----------------------|------------------------------|-------------------------------|
| Type                  | Synchronous (Blocking)       | Asynchronous (Non-blocking)   |
| Use with FastAPI      | Not Recommended              | Recommended                 |
| Performance           | Slower under load            | Scales well with concurrency  |
| Suitable for          | Scripts, simple apps         | Async APIs (like FastAPI)     |
