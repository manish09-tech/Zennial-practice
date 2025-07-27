import logging
from fastapi import FastAPI, HTTPException
from schemas import UserRegister
from database import collection
from datetime import datetime
from models import hash_password, create_user
from pymongo.errors import DuplicateKeyError

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("user.log"),
        logging.StreamHandler() 
    ]
)

# make sure the email field is unique
collection.create_index("email", unique=True)

@app.post("/register")
async def register_user(user: UserRegister):
    logging.info(f"Received registration request for: {user.email}")
    
    if collection.find_one({"email": user.email}):
        logging.warning(f"Duplicate registration attempt for: {user.email}")
        raise HTTPException(status_code=400, detail="EmailID already registered")

    user_dict = user.model_dump()
    user_dict["password"] = hash_password(user.password)
    user_dict["dob"] = datetime.combine(user.dob, datetime.min.time())
    user_dict["doj"] = datetime.combine(user.doj, datetime.min.time())

    try:
        create_user(user_dict)
        logging.info(f"User registered successfully: {user.email}")
        return {"message": "User registered successfully"}
    except DuplicateKeyError:
        logging.error(f"DuplicateKeyError for: {user.email}")
        raise HTTPException(status_code=400, detail="User with this emailID already exists")
    except Exception as e:
        logging.exception(f"Unexpected error during registration of {user.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
