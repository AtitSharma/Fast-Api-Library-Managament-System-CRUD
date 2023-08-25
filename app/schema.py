from pydantic import BaseModel, EmailStr,ConfigDict
from typing import Optional
from datetime import datetime
from typing import Type,Any,TypeVar

T=TypeVar("T")

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    
class UserDetails(BaseModel):
    email: EmailStr
    username:str
    


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
       
class Rolename(BaseModel):
    name : str

class StatusSchema(BaseModel):
    code:str | None
    status: str | None
    data: T | None
    message : str | None
    
    


        
    
    