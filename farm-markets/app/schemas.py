from pydantic import BaseModel, EmailStr
from typing import Optional

# Users
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str # farmer or buyer

class UserOut(BaseModel):
    id: str 
    name: str
    email: EmailStr
    role: str
    created_at: str # ISO formatted datetime string

class LoginData(BaseModel):
        email: EmailStr
        password: str

class Token(BaseModel):
        access_token: str
        token_type: str = "bearer"


# Products
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int


class ProductOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    farmer_id: str
    created_at: str


# Orders
class OrderCreate(BaseModel):
    product_id: str
    quantity: int

class OrderOut(BaseModel):
    id: str
    buyer_id: str
    farmer_id: str
    product_id: str
    quantity: int
    total_price: float
    status: str
    created_at: str
    