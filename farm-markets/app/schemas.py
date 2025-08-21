from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

# Users
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str # farmer or buyer

