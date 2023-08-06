from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr


class TokenData(BaseModel):
    id: Optional[int] = None


class BookCreate(BaseModel):
    title: str
    description: str


class BookDetail(BookCreate):
    id: int
    author: UserOut
    created_at: datetime


class UserRole(BaseModel):
    user_id: int
    role_id: int


class RoleCreate(BaseModel):
    name: str
