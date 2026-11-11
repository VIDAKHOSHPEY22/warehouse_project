"""
services/report_service.py
----------------------------------------------------------------
گزارش‌های عملیاتی سیستم. تمام کوئری‌های تجمیعی (aggregate) اینجا
متمرکز شده‌اند تا Routeها فقط فراخوانی کنند.
----------------------------------------------------------------
"""
from datetime import date, timedelta

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.batch import Batch
from app.models.item import Item
from app.models.location import Location
from app.models.transaction import Transaction
from app.models.enums import TransactionType


def current_stock_report(db: Session) -> list[dict]:
    """موجودی لحظه‌ای تجمیع‌شده به ازای هر کالا."""
    rows = db.execute(
        select(
            Item.id,
            Item.code,
            Item.name,
            Item.unit,
            Item.min_stock,
            func.coalesce(func.sum(Batch.quantity_on_hand), 0).label("total_on_hand"),
            func.coalesce(func.sum(Batch.quantity_allocated), 0).label("total_allocated"),
        )
        .outerjoin(Batch, Batch.item_id == Item.id)
        .where(Item.is_active.is_(True))
        .group_by(Item.id)
        .order_by(Item.name)
    ).all()

    result = []
    for r in rows:
        total_available = r.total_on_hand - r.total_allocated
        result.append({
            "item_id": r.id,
            "item_code": r.code,
            "item_name": r.name,
            "unit": r.unit,
            "total_on_hand": r.total_on_hand,
            "total_allocated": r.total_allocated,
            "total_available": total_available,
            "min_stock": r.min_stock,
            "is_low_stock": total_available < r.min_stock,
        })
    return result


def low_stock_report(db: Session) -> list[dict]:
    """فقط اقلامی که موجودی قابل تخصیص آن‌ها از حداقل تعیین‌شده کمتر است."""
    return [row for row in current_stock_report(db) if row["is_low_stock"]]


def expiring_batches_report(db: Session, days_ahead: int = 30) -> list[dict]:
    """بچ‌هایی که تا `days_ahead` روز آینده منقضی می‌شوند - برای اولویت‌بندی توزیع (FEFO)."""
    limit_date = date.today() + timedelta(days=days_ahead)
    rows = db.execute(
        select(Batch, Item.name.label("item_name"), Location.name.label("location_name"))
        .join(Item, Item.id == Batch.item_id)
        .join(Location, Location.id == Batch.location_id)
        .where(Batch.expiry_date.is_not(None), Batch.expiry_date <= limit_date, Batch.quantity_on_hand > 0)
        .order_by(Batch.expiry_date.asc())
    ).all()

    return [
        {
            "batch_id": b.Batch.id,
            "item_name": b.item_name,
            "location_name": b.location_name,
            "batch_no": b.Batch.batch_no,
            "expiry_date": b.Batch.expiry_date,
            "quantity_on_hand": b.Batch.quantity_on_hand,
        }
        for b in rows
    ]


def turnover_report(db: Session) -> list[dict]:
    """جمع کل ورودی و خروجی هر کالا از ابتدای فعالیت - برای سنجش گردش کالا."""
    received = db.execute(
        select(Transaction.item_id, func.sum(Transaction.quantity))
        .where(Transaction.type == TransactionType.RECEIPT)
        .group_by(Transaction.item_id)
    ).all()
    issued = db.execute(
        select(Transaction.item_id, func.sum(Transaction.quantity))
        .where(Transaction.type == TransactionType.ISSUE)
        .group_by(Transaction.item_id)
    ).all()

    received_map = {item_id: qty for item_id, qty in received}
    issued_map = {item_id: qty for item_id, qty in issued}
    item_ids = set(received_map) | set(issued_map)

    items = {i.id: i.name for i in db.execute(select(Item).where(Item.id.in_(item_ids))).scalars().all()}

    return [
        {
            "item_id": item_id,
            "item_name": items.get(item_id, "نامشخص"),
            "total_received": received_map.get(item_id, 0),
            "total_issued": issued_map.get(item_id, 0),
        }
        for item_id in item_ids
    ]
