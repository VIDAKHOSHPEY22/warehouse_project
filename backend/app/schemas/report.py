"""schemas/report.py - ساختار خروجی گزارش‌ها"""
from datetime import date

from pydantic import BaseModel


class StockReportRow(BaseModel):
    item_id: int
    item_code: str
    item_name: str
    unit: str
    total_on_hand: int
    total_allocated: int
    total_available: int
    min_stock: int
    is_low_stock: bool


class LowStockRow(BaseModel):
    item_id: int
    item_code: str
    item_name: str
    total_available: int
    min_stock: int


class ExpiringBatchRow(BaseModel):
    batch_id: int
    item_name: str
    location_name: str
    batch_no: str | None
    expiry_date: date | None
    quantity_on_hand: int


class TurnoverRow(BaseModel):
    item_id: int
    item_name: str
    total_received: int
    total_issued: int
