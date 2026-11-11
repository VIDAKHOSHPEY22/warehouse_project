"""
api/routes/transactions.py
----------------------------------------------------------------
Endpointهای عملیاتی اصلی انبار: دریافت، تخصیص، خروج، جابجایی و
اصلاح موجودی. منطق واقعی در app/services/inventory_service.py است؛
این فایل فقط نگاشت HTTP <-> Service را انجام می‌دهد.
----------------------------------------------------------------
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.transaction import Transaction
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.transaction import (
    ReceiptCreate, AllocationCreate, IssueCreate, TransferCreate, AdjustmentCreate, TransactionRead,
)
from app.api.deps import require_roles, get_current_user
from app.services import inventory_service

router = APIRouter(prefix="/api/transactions", tags=["تراکنش‌های انبار"])


@router.get("", response_model=list[TransactionRead], dependencies=[Depends(get_current_user)])
def list_transactions(
    db: Session = Depends(get_db),
    item_id: int | None = Query(default=None),
    mission_id: int | None = Query(default=None),
    limit: int = Query(default=100, le=500),
):
    query = db.query(Transaction)
    if item_id:
        query = query.filter(Transaction.item_id == item_id)
    if mission_id:
        query = query.filter(Transaction.mission_id == mission_id)
    return query.order_by(Transaction.created_at.desc()).limit(limit).all()


@router.post("/receive", response_model=TransactionRead,
             dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.WAREHOUSE))])
def receive(payload: ReceiptCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """ثبت ورود کالای جدید (Receiving)."""
    return inventory_service.receive_stock(db, payload, current_user.id)


@router.post("/allocate", response_model=TransactionRead,
             dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR))])
def allocate(payload: AllocationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """تخصیص کالا به یک مأموریت (رزرو، بدون خروج فیزیکی)."""
    return inventory_service.allocate_stock(db, payload, current_user.id)


@router.post("/issue", response_model=TransactionRead,
             dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.WAREHOUSE))])
def issue(payload: IssueCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """خروج نهایی کالا از انبار (تحویل به گیرنده)."""
    return inventory_service.issue_stock(db, payload, current_user.id)


@router.post("/transfer", response_model=TransactionRead,
             dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.WAREHOUSE))])
def transfer(payload: TransferCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """جابجایی موجودی بین دو مکان داخل انبار."""
    return inventory_service.transfer_stock(db, payload, current_user.id)


@router.post("/adjust", response_model=TransactionRead,
             dependencies=[Depends(require_roles(UserRole.ADMIN))])
def adjust(payload: AdjustmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """اصلاح موجودی پس از انبارگردانی فیزیکی (فقط ادمین)."""
    return inventory_service.adjust_stock(db, payload, current_user.id)
