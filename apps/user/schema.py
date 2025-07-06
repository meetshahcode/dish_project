from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }
    


class UserRegister(UserBase):
    password: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserLoginResponse(User):
    pass

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

class JwtTokenSchema(BaseModel):
    token: str
    payload: dict
    expire: datetime


