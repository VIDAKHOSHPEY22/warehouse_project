"""
models/audit.py
----------------------------------------------------------------
AuditLog = لاگ تغییرات حیاتی سیستم (ایجاد/ویرایش/حذف کاربران،
اقلام، مکان‌ها و ...) جدا از Transaction که فقط گردش کالا را
پوشش می‌دهد. این جدول برای پاسخگویی به سوال "چه کسی، چه زمانی،
چه تغییری داد؟" استفاده می‌شود.
----------------------------------------------------------------
"""
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(64), nullable=False)      # create/update/delete/login
    entity: Mapped[str] = mapped_column(String(64), nullable=False)      # نام موجودیت: item, user, location, ...
    entity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    details: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="audit_logs")
