from fastapi import FastAPI, HTTPException
from schemas import UserRegister
from database import collection
from datetime import datetime
from models import hash_password, create_user
from pymongo.errors import DuplicateKeyError

app = FastAPI()

# make sure the email field is unique
collection.create_index("email", unique=True)

@app.post("/register")
def register_user(user: UserRegister):
    if collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="EmailID already registered")

    user_dict = user.model_dump()
    user_dict["password"] = hash_password(user.password)

    # Convert date to datetime
    user_dict["dob"] = datetime.combine(user.dob, datetime.min.time())
    user_dict["doj"] = datetime.combine(user.doj, datetime.min.time())

    try:
        create_user(user_dict)
        return {"message": "User registered successfully"}
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="User with this emailID already exists")

