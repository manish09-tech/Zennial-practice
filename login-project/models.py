from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str]
    password: str
    dob: date
    doj: date
    address: str
    comments: Optional[str] = None
    active: bool


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

