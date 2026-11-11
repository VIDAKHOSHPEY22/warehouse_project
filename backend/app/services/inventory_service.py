"""
services/inventory_service.py
----------------------------------------------------------------
لایه منطق کسب‌وکار (Business Logic Layer) انبار.

چرا این لایه جدا از Route هاست؟
    Routeها (app/api/routes) فقط باید ورودی را اعتبارسنجی کنند و
    پاسخ HTTP بدهند. تمام قوانین کسب‌وکار (مثلا "نمی‌توان بیشتر از
    موجودی، تخصیص داد") اینجا متمرکز است تا:
      1) قابل تست باشد بدون نیاز به FastAPI/HTTP
      2) در آینده اگر یک CLI یا Worker جداگانه لازم شد، بتوان از
         همین توابع استفاده کرد بدون تکرار کد.

اصل طلایی این ماژول:
    هر تغییر موجودی (افزایش/کاهش quantity_on_hand یا
    quantity_allocated) هم زمان یک رکورد Transaction ثبت می‌کند.
    این دو عملیات همیشه در یک تراکنش دیتابیسی (db.commit) با هم
    انجام می‌شوند تا هرگز موجودی و لاگ گردش از هم جدا نیفتند.
----------------------------------------------------------------
"""
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.batch import Batch
from app.models.item import Item
from app.models.location import Location
from app.models.mission import Mission
from app.models.transaction import Transaction
from app.models.enums import TransactionType, MissionStatus
from app.schemas.transaction import (
    ReceiptCreate,
    AllocationCreate,
    IssueCreate,
    TransferCreate,
    AdjustmentCreate,
)


def _get_or_404(db: Session, model, obj_id: int, name: str):
    obj = db.get(model, obj_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{name} با شناسه {obj_id} یافت نشد")
    return obj


def receive_stock(db: Session, payload: ReceiptCreate, user_id: int) -> Transaction:
    """
    ثبت ورود کالا (Receiving).
    اگر بچ مشابهی (همان کالا+مکان+شماره بچ+تاریخ انقضا) از قبل
    وجود داشته باشد به آن اضافه می‌شود، در غیر این صورت بچ جدید
    ساخته می‌شود.
    """
    _get_or_404(db, Item, payload.item_id, "کالا")
    _get_or_404(db, Location, payload.location_id, "مکان")

    existing = db.execute(
        select(Batch).where(
            Batch.item_id == payload.item_id,
            Batch.location_id == payload.location_id,
            Batch.batch_no == payload.batch_no,
            Batch.expiry_date == payload.expiry_date,
        )
    ).scalar_one_or_none()

    if existing:
        existing.quantity_on_hand += payload.quantity
        batch = existing
    else:
        batch = Batch(
            item_id=payload.item_id,
            location_id=payload.location_id,
            batch_no=payload.batch_no,
            expiry_date=payload.expiry_date,
            quantity_on_hand=payload.quantity,
            quantity_allocated=0,
        )
        db.add(batch)
        db.flush()  # برای گرفتن batch.id قبل از commit نهایی

    tx = Transaction(
        type=TransactionType.RECEIPT,
        item_id=payload.item_id,
        batch_id=batch.id,
        user_id=user_id,
        quantity=payload.quantity,
        source=payload.source,
        note=payload.note,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def allocate_stock(db: Session, payload: AllocationCreate, user_id: int) -> Transaction:
    """
    تخصیص (رزرو) بخشی از موجودی یک بچ به یک مأموریت.
    فقط quantity_allocated افزایش می‌یابد؛ موجودی فیزیکی تغییری
    نمی‌کند تا زمانی که واقعا خروج (Issue) ثبت شود.
    """
    batch = _get_or_404(db, Batch, payload.batch_id, "بچ")
    mission = _get_or_404(db, Mission, payload.mission_id, "مأموریت")

    if payload.quantity > batch.quantity_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"موجودی قابل تخصیص کافی نیست. موجودی قابل تخصیص: {batch.quantity_available}",
        )

    batch.quantity_allocated += payload.quantity
    if mission.status == MissionStatus.DRAFT:
        mission.status = MissionStatus.ALLOCATED

    tx = Transaction(
        type=TransactionType.ALLOCATION,
        item_id=batch.item_id,
        batch_id=batch.id,
        mission_id=mission.id,
        user_id=user_id,
        quantity=payload.quantity,
        note=payload.note,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def issue_stock(db: Session, payload: IssueCreate, user_id: int) -> Transaction:
    """
    خروج نهایی کالا از انبار (تحویل به گیرنده/مقصد).
    اگر تراکنش به مأموریت مرتبط باشد و قبلا برای آن تخصیص ثبت شده
    بود، quantity_allocated هم متناسب کاهش می‌یابد.
    """
    batch = _get_or_404(db, Batch, payload.batch_id, "بچ")

    if payload.quantity > batch.quantity_on_hand:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"موجودی فیزیکی کافی نیست. موجودی فعلی: {batch.quantity_on_hand}",
        )

    batch.quantity_on_hand -= payload.quantity
    # اگر مقدار تخصیص‌یافته بیشتر از صفر بود، متناسب با خروج کم می‌شود
    if batch.quantity_allocated > 0:
        batch.quantity_allocated = max(0, batch.quantity_allocated - payload.quantity)

    mission = None
    if payload.mission_id:
        mission = _get_or_404(db, Mission, payload.mission_id, "مأموریت")
        mission.status = MissionStatus.DELIVERED

    tx = Transaction(
        type=TransactionType.ISSUE,
        item_id=batch.item_id,
        batch_id=batch.id,
        mission_id=mission.id if mission else None,
        user_id=user_id,
        quantity=payload.quantity,
        recipient=payload.recipient,
        destination=payload.destination,
        note=payload.note,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def transfer_stock(db: Session, payload: TransferCreate, user_id: int) -> Transaction:
    """جابجایی مقداری از یک بچ به مکان دیگر (بچ مقصد در صورت نبود ساخته می‌شود)."""
    batch = _get_or_404(db, Batch, payload.batch_id, "بچ")
    _get_or_404(db, Location, payload.to_location_id, "مکان مقصد")

    if payload.quantity > batch.quantity_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="موجودی قابل جابجایی کافی نیست (مقدار تخصیص‌یافته قابل جابجایی نیست)",
        )

    dest = db.execute(
        select(Batch).where(
            Batch.item_id == batch.item_id,
            Batch.location_id == payload.to_location_id,
            Batch.batch_no == batch.batch_no,
            Batch.expiry_date == batch.expiry_date,
        )
    ).scalar_one_or_none()

    batch.quantity_on_hand -= payload.quantity
    if dest:
        dest.quantity_on_hand += payload.quantity
    else:
        dest = Batch(
            item_id=batch.item_id,
            location_id=payload.to_location_id,
            batch_no=batch.batch_no,
            expiry_date=batch.expiry_date,
            quantity_on_hand=payload.quantity,
            quantity_allocated=0,
        )
        db.add(dest)
        db.flush()

    tx = Transaction(
        type=TransactionType.TRANSFER,
        item_id=batch.item_id,
        batch_id=batch.id,
        user_id=user_id,
        quantity=payload.quantity,
        note=f"انتقال به مکان #{payload.to_location_id}. {payload.note or ''}".strip(),
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def adjust_stock(db: Session, payload: AdjustmentCreate, user_id: int) -> Transaction:
    """اصلاح موجودی پس از انبارگردانی فیزیکی. delta می‌تواند منفی باشد."""
    batch = _get_or_404(db, Batch, payload.batch_id, "بچ")

    new_qty = batch.quantity_on_hand + payload.delta
    if new_qty < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="موجودی نمی‌تواند منفی شود")
    if new_qty < batch.quantity_allocated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="موجودی جدید نمی‌تواند کمتر از مقدار تخصیص‌یافته باشد",
        )

    batch.quantity_on_hand = new_qty

    tx = Transaction(
        type=TransactionType.ADJUSTMENT,
        item_id=batch.item_id,
        batch_id=batch.id,
        user_id=user_id,
        quantity=abs(payload.delta),
        note=f"{'افزایش' if payload.delta >= 0 else 'کاهش'} اصلاحی. {payload.note or ''}".strip(),
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx
