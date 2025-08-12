from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class DetectionBase(BaseModel):
    filename: str
    prediction: str
    confidence: float

class DetectionCreate(DetectionBase):
    pass

class Detection(DetectionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True