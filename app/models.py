from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from .database import Base


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(length=255), nullable=False, unique=True)
    password = Column(String(length=255), nullable=False)
    hashed_password = Column(String(length=255), nullable=False)
    is_active = Column(Boolean, default=False)
    created_date = Column(DateTime, default=func.now())
    last_login_date = Column(DateTime, nullable=True)
