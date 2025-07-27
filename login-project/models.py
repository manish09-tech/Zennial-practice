from passlib.context import CryptContext
from database import collection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Insert user
def create_user(user_data: dict):
    collection.insert_one(user_data)
