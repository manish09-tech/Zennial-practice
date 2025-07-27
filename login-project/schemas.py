from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserRegister(BaseModel):
    first_name: str
    last_name: str 
    email: EmailStr
    phone: str
    password: str
    dob: date
    doj: date
    address: str
    comments: Optional[str] = None
    active: bool
