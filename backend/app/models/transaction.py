"""
models/transaction.py
----------------------------------------------------------------
Transaction = دفتر کل گردش کالا (Ledger). هر رویداد ورود، خروج،
تخصیص یا اصلاح موجودی، یک رکورد تراکنش تولید می‌کند و
هرگز حذف یا ویرایش نمی‌شود (Append-Only) تا سابقه کامل و
قابل حسابرسی (Audit) بماند.

quantity: همیشه مثبت ذخیره می‌شود؛ نوع تراکنش (type) مشخص می‌کند
جهت تغییر موجودی چیست (افزایشی یا کاهشی) - این منطق در
services/inventory_service.py پیاده‌سازی شده است.
----------------------------------------------------------------
"""
from datetime import datetime, timezone

from sqlalchemy import String, Integer, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import TransactionType


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[TransactionType] = mapped_column(SAEnum(TransactionType), nullable=False, index=True)

    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False, index=True)
    batch_id: Mapped[int | None] = mapped_column(ForeignKey("batches.id"), nullable=True, index=True)
    mission_id: Mapped[int | None] = mapped_column(ForeignKey("missions.id"), nullable=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # اطلاعات تکمیلی بسته به نوع تراکنش
    source: Mapped[str | None] = mapped_column(String(128), nullable=True)       # منبع ورود (اهداکننده/تأمین‌کننده)
    recipient: Mapped[str | None] = mapped_column(String(128), nullable=True)    # گیرنده در زمان خروج
    destination: Mapped[str | None] = mapped_column(String(128), nullable=True)  # مقصد در زمان خروج
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    item = relationship("Item", back_populates="transactions")
    batch = relationship("Batch")
    mission = relationship("Mission", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
