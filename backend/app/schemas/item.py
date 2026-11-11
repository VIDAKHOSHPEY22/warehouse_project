"""schemas/item.py"""
from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    code: str
    name: str
    category: str | None = None
    unit: str = "عدد"
    expiry_required: bool = False
    min_stock: int = 0
    unit_value: float | None = None
    description: str | None = None
    is_active: bool = True


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    category: str | None = None
    unit: str | None = None
    expiry_required: bool | None = None
    min_stock: int | None = None
    unit_value: float | None = None
    description: str | None = None
    is_active: bool | None = None


class ItemRead(ItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    total_on_hand: int = 0    # جمع موجودی فیزیکی از همه بچ‌ها (در سرویس محاسبه می‌شود)
    total_available: int = 0  # جمع موجودی قابل تخصیص
