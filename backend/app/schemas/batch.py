"""schemas/batch.py"""
from datetime import date

from pydantic import BaseModel, ConfigDict

from app.schemas.item import ItemRead
from app.schemas.location import LocationRead


class BatchBase(BaseModel):
    item_id: int
    location_id: int
    batch_no: str | None = None
    expiry_date: date | None = None


class BatchCreate(BatchBase):
    quantity_on_hand: int = 0


class BatchRead(BatchBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    quantity_on_hand: int
    quantity_allocated: int
    quantity_available: int
    item: ItemRead | None = None
    location: LocationRead | None = None
