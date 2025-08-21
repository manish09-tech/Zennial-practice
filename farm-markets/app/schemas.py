from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

# Users
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str # farmer or buyer

class UserOut(BaseModel):
    _id: str = Field(alias="_id")
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    class LoginData(BaseModel):
        email: EmailStr
        password: str

    class Token(BaseModel):
        access_token: str
        token_type: str = "bearer"


# Products
class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int

class ProductOut(BaseModel):
    _id: str = Field(alias="_id")
    name: str
    price: float
    quantity: int
    created_at: datetime

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Orders
class OrderCreate(BaseModel):
    product_id: str
    quantity: int

class OrderOut(BaseModel):
    _id: str = Field(alias="_id")
    product_id: str
    buyer_id: str
    quantity: int
    total_price: float
    created_at: datetime
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }