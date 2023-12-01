from pydantic import BaseModel, EmailStr, SecretStr, field_validator
from typing import Optional
from passlib.context import CryptContext

from src.utils.schemas import UUIDView

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserMiniView",
    "UserView",
]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserPassHashMixin:
    @field_validator("password")
    def password_validator(cls, v):
        if v:
            print(v.get_secret_value())
            return pwd_context.hash(v.get_secret_value())
        return v

class UserCreate(BaseModel, UserPassHashMixin):
    email: EmailStr
    password: SecretStr
    first_name: str
    last_name: str
    is_active: bool = True


class UserUpdate(BaseModel, UserPassHashMixin):
    email: Optional[EmailStr] = None
    password: Optional[SecretStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserMiniView(BaseModel, UUIDView):
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class UserView(BaseModel, UUIDView):
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool = True

    class Config:
        from_attributes = True


class UserMeView(BaseModel, UUIDView):
    email: str
    first_name: str
    last_name: str
    is_active: bool

    class Config:
        from_attributes = True
