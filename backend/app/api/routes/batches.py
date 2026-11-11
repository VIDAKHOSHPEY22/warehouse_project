"""
api/routes/batches.py - مشاهده موجودی بچ‌ها (خواندنی - تغییرات فقط از طریق transactions انجام می‌شود)
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.batch import Batch
from app.schemas.batch import BatchRead
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/batches", tags=["بچ / موجودی"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[BatchRead])
def list_batches(
    db: Session = Depends(get_db),
    item_id: int | None = Query(default=None),
    location_id: int | None = Query(default=None),
    only_available: bool = Query(default=False, description="فقط بچ‌هایی که موجودی قابل تخصیص دارند"),
):
    query = db.query(Batch)
    if item_id:
        query = query.filter(Batch.item_id == item_id)
    if location_id:
        query = query.filter(Batch.location_id == location_id)
    batches = query.all()
    if only_available:
        batches = [b for b in batches if b.quantity_available > 0]
    return batches
