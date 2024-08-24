from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AccountBase(BaseModel):
    id: int
    name: str
    email: str


class AccountCreate(AccountBase):
    id: int
    password: str
    created_date: datetime
    is_active: bool


class AccountUpdate(AccountBase):
    id: int
    password: str
    is_active: bool


class AccountResponse(AccountBase):
    id: int
    created_date: datetime
    last_login_date: Optional[datetime] = None
    is_active: bool

    class Config:
        orm_model = True


class AccountRegister(AccountBase):
    password: str
    hashed_password: str
