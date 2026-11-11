"""
schemas/user.py
----------------------------------------------------------------
الگوی معمول این پروژه برای هر موجودیت:
    Base    -> فیلدهای مشترک
    Create  -> فیلدهای لازم برای ساخت (شامل رمز خام قبل از هش)
    Update  -> همه فیلدها اختیاری (برای PATCH/PUT جزئی)
    Read    -> خروجی API (from_attributes=True یعنی مستقیم از ORM ساخته می‌شود)
----------------------------------------------------------------
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import UserRole


class UserBase(BaseModel):
    username: str
    full_name: str
    role: UserRole = UserRole.WAREHOUSE
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None
    password: str | None = None  # اگر پر شود، رمز عوض می‌شود


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
