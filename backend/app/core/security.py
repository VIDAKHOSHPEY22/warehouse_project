"""
core/security.py
----------------------------------------------------------------
توابع مربوط به امنیت:
    - هش کردن و بررسی رمز عبور (bcrypt از طریق passlib)
    - ساخت و اعتبارسنجی توکن JWT
----------------------------------------------------------------
"""
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """رمز عبور خام را به هش bcrypt تبدیل می‌کند - هرگز رمز خام ذخیره نشود."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """رمز واردشده توسط کاربر را با هش ذخیره‌شده در دیتابیس مقایسه می‌کند."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, extra_claims: dict[str, Any] | None = None) -> str:
    """
    یک توکن JWT می‌سازد.
    subject: معمولا username کاربر
    extra_claims: داده‌های اضافی مثل نقش کاربر (role) که در توکن جاسازی می‌شود
    تا در هر درخواست، بدون نیاز به کوئری اضافه دیتابیس، نقش کاربر مشخص باشد.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": expire}
    if extra_claims:
        to_encode.update(extra_claims)
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any] | None:
    """توکن را رمزگشایی می‌کند. اگر منقضی یا نامعتبر باشد None برمی‌گرداند."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
