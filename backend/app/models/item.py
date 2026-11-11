"""
models/item.py
----------------------------------------------------------------
تعریف کالا (SKU - Stock Keeping Unit).
این جدول "شناسنامه کالا" است؛ موجودی واقعی در جدول Batch نگهداری
می‌شود چون یک کالا می‌تواند در چند بچ/مکان/تاریخ انقضای متفاوت باشد.
----------------------------------------------------------------
"""
from sqlalchemy import String, Boolean, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)  # کد SKU
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    category: Mapped[str | None] = mapped_column(String(64), nullable=True)  # غذا/پوشاک/بهداشت/...
    unit: Mapped[str] = mapped_column(String(16), nullable=False, default="عدد")  # عدد/کارتن/کیلوگرم
    expiry_required: Mapped[bool] = mapped_column(Boolean, default=False)  # آیا کالا تاریخ انقضا دارد؟
    min_stock: Mapped[int] = mapped_column(Integer, default=0)  # حداقل موجودی برای هشدار
    unit_value: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)  # ارزش تقریبی هر واحد (اختیاری - گزارش مالی)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    batches = relationship("Batch", back_populates="item", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="item")
