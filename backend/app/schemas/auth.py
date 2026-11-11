"""
schemas/auth.py - مدل‌های ورودی/خروجی مربوط به احراز هویت
"""
from pydantic import BaseModel

from app.models.enums import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    role: UserRole | None = None
