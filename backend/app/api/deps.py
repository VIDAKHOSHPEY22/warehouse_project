"""
api/deps.py
----------------------------------------------------------------
Dependencyهای مشترک FastAPI:
    - get_current_user: از هدر Authorization توکن را می‌خواند و
      کاربر متناظر را برمی‌گرداند.
    - require_roles(...): یک Dependency factory که فقط نقش‌های
      مشخص‌شده را مجاز می‌کند (RBAC در سطح Route).
----------------------------------------------------------------
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.models.enums import UserRole

# tokenUrl فقط برای مستندات Swagger استفاده می‌شود (دکمه Authorize)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="اعتبارسنجی ناموفق بود",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    username = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user


def require_roles(*allowed_roles: UserRole):
    """
    استفاده:
        @router.post("/items", dependencies=[Depends(require_roles(UserRole.ADMIN))])
    فقط کاربرانی که نقششان در allowed_roles باشد اجازه دسترسی دارند.
    """
    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی لازم برای این عملیات را ندارید",
            )
        return current_user
    return checker
