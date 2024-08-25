from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class AccountRegister(BaseModel):
    name: str
    email: str
    password: str


class AccountFullUpdate(BaseModel):
    name: str
    email: str
    password: str
    is_active: bool


class AccountPartialUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class AccountResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    created_date: datetime
    last_login_date: Optional[datetime] = None
    hashed_password: str
