"""
models/user.py
----------------------------------------------------------------
مدل کاربر سیستم.
هر کاربر یک نقش (role) دارد که سطح دسترسی او را در لایه API
(دیده در app/api/deps.py) تعیین می‌کند.
----------------------------------------------------------------
"""
from datetime import datetime, timezone

from sqlalchemy import String, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), nullable=False, default=UserRole.WAREHOUSE)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # ارتباط معکوس با تراکنش‌ها و لاگ‌ها (برای دیدن سوابق کاربر)
    transactions = relationship("Transaction", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
