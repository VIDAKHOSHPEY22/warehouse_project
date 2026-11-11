"""
api/routes/auth.py - ورود به سیستم و صدور توکن JWT
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserRead
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/auth", tags=["احراز هویت"])


@router.post("/login", response_model=Token, summary="ورود و دریافت توکن")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    از فرمت استاندارد OAuth2PasswordRequestForm استفاده می‌کند
    (فیلدهای username و password به صورت form-data) تا با Swagger UI
    و کتابخانه‌های استاندارد سازگار باشد.
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="نام کاربری یا رمز عبور اشتباه است")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="حساب کاربری غیرفعال است")

    token = create_access_token(subject=user.username, extra_claims={"role": user.role.value})
    return Token(access_token=token)


@router.get("/me", response_model=UserRead, summary="اطلاعات کاربر فعلی")
def read_me(current_user: User = Depends(get_current_user)):
    return current_user
