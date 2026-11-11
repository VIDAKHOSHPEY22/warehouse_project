"""
models/batch.py
----------------------------------------------------------------
Batch (بچ/لات) = موجودی واقعیِ یک کالای مشخص، در یک مکان مشخص،
با یک شماره بچ و تاریخ انقضای مشخص (در صورت نیاز).

چرا Batch جدا از Item؟
    یک کالا (مثلا "کنسرو لوبیا") ممکن است چند بار وارد انبار شده
    باشد، هر بار با تاریخ انقضا و منبع تأمین متفاوت، و در مکان‌های
    مختلفی چیده شده باشد. برای رهگیری دقیق (FEFO: First-Expire-
    First-Out) باید هر محموله را جدا نگه داشت.

quantity_on_hand: موجودی فیزیکی واقعی در انبار
quantity_allocated: مقداری که به یک مأموریت تخصیص داده شده ولی هنوز
    از انبار خارج نشده (رزرو‌شده)
quantity_available (property): مقدار واقعا قابل تخصیص = on_hand - allocated
----------------------------------------------------------------
"""
from datetime import date

from sqlalchemy import String, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Batch(Base):
    __tablename__ = "batches"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False, index=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), nullable=False, index=True)

    batch_no: Mapped[str | None] = mapped_column(String(64), nullable=True)  # شماره محموله/بچ (اختیاری)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    quantity_on_hand: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    quantity_allocated: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    item = relationship("Item", back_populates="batches")
    location = relationship("Location", back_populates="batches")

    @property
    def quantity_available(self) -> int:
        """مقدار واقعا قابل تخصیص به مأموریت جدید."""
        return max(self.quantity_on_hand - self.quantity_allocated, 0)
