from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class StudentBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class StudentCreate(StudentBase):
    password: str

class StudentDisplay(StudentBase):
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class StudentUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    # Add other fields that can be updated, but NOT username or password here.
