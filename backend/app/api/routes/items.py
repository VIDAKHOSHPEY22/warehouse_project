"""
api/routes/items.py - مدیریت شناسنامه کالا (SKU)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.item import Item
from app.models.batch import Batch
from app.models.enums import UserRole
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.api.deps import require_roles, get_current_user

router = APIRouter(prefix="/api/items", tags=["اقلام (SKU)"])


def _to_read(db: Session, item: Item) -> ItemRead:
    """موجودی تجمیعی از بچ‌ها را به خروجی کالا اضافه می‌کند."""
    totals = db.execute(
        select(
            func.coalesce(func.sum(Batch.quantity_on_hand), 0),
            func.coalesce(func.sum(Batch.quantity_allocated), 0),
        ).where(Batch.item_id == item.id)
    ).one()
    on_hand, allocated = totals
    read = ItemRead.model_validate(item)
    read.total_on_hand = on_hand
    read.total_available = on_hand - allocated
    return read


@router.get("", response_model=list[ItemRead], dependencies=[Depends(get_current_user)])
def list_items(db: Session = Depends(get_db), search: str | None = None):
    query = db.query(Item)
    if search:
        query = query.filter(Item.name.ilike(f"%{search}%") | Item.code.ilike(f"%{search}%"))
    items = query.order_by(Item.name).all()
    return [_to_read(db, i) for i in items]


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR))])
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    if db.query(Item).filter(Item.code == payload.code).first():
        raise HTTPException(status_code=400, detail="کد کالا تکراری است")
    item = Item(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return _to_read(db, item)


@router.patch("/{item_id}", response_model=ItemRead,
              dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR))])
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="کالا یافت نشد")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return _to_read(db, item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_roles(UserRole.ADMIN))])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="کالا یافت نشد")
    db.delete(item)
    db.commit()
