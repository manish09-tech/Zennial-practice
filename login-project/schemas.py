from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# User Registration
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
    active: bool = True

# Change Password (Logged-in)
class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str

# Forgot Password (via Email)
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

# Reset Password (via Token)
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
