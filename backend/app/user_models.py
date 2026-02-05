from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from passlib.context import CryptContext
import re


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def validate_email(email: str) -> str:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")
    return email


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, min_length=5, max_length=100)
    username: str = Field(unique=True, index=True, min_length=3, max_length=50)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    password: str = Field(min_length=6)

    def __init__(self, **data):
        super().__init__(**data)
        # Validate email format
        self.email = validate_email(self.email)

    @property
    def password_hash(self):
        return pwd_context.hash(self.password)


class UserLogin(BaseModel):
    email: str
    password: str

    def __init__(self, **data):
        super().__init__(**data)
        # Validate email format
        self.email = validate_email(self.email)


class UserResponse(UserBase):
    id: int
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


class UserMeResponse(BaseModel):
    user_id: int
    username: Optional[str] = None
    email: Optional[str] = None