"""
schemas/transaction.py
----------------------------------------------------------------
برای هر نوع عملیات انبار، یک اسکیمای ورودی اختصاصی تعریف شده تا
فقط فیلدهای مرتبط با آن عملیات از کاربر خواسته شود (مثلا در Receipt
نیازی به mission_id نیست ولی در Allocation/Issue لازم است).
----------------------------------------------------------------
"""
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import TransactionType


class ReceiptCreate(BaseModel):
    """ثبت ورود کالای جدید به انبار (ساخت خودکار Batch در صورت نیاز)."""
    item_id: int
    location_id: int
    quantity: int = Field(gt=0)
    batch_no: str | None = None
    expiry_date: date | None = None
    source: str | None = None
    note: str | None = None


class AllocationCreate(BaseModel):
    """تخصیص (رزرو) مقداری از یک بچ مشخص به یک مأموریت."""
    batch_id: int
    mission_id: int
    quantity: int = Field(gt=0)
    note: str | None = None


class IssueCreate(BaseModel):
    """خروج نهایی کالا از انبار - می‌تواند مرتبط با مأموریت باشد یا نباشد."""
    batch_id: int
    quantity: int = Field(gt=0)
    mission_id: int | None = None
    recipient: str | None = None
    destination: str | None = None
    note: str | None = None


class TransferCreate(BaseModel):
    """جابجایی موجودی یک بچ از مکان فعلی به مکان دیگر."""
    batch_id: int
    to_location_id: int
    quantity: int = Field(gt=0)
    note: str | None = None


class AdjustmentCreate(BaseModel):
    """اصلاح موجودی بعد از شمارش فیزیکی. delta می‌تواند مثبت یا منفی باشد."""
    batch_id: int
    delta: int  # مثبت = افزایش، منفی = کاهش
    note: str | None = None


class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type: TransactionType
    item_id: int
    batch_id: int | None
    mission_id: int | None
    user_id: int
    quantity: int
    source: str | None
    recipient: str | None
    destination: str | None
    note: str | None
    created_at: datetime
