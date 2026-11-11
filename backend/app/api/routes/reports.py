"""
api/routes/reports.py - گزارش‌های عملیاتی
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.report import StockReportRow, LowStockRow, ExpiringBatchRow, TurnoverRow
from app.api.deps import get_current_user
from app.services import report_service

router = APIRouter(prefix="/api/reports", tags=["گزارش‌ها"], dependencies=[Depends(get_current_user)])


@router.get("/current-stock", response_model=list[StockReportRow], summary="موجودی لحظه‌ای همه اقلام")
def current_stock(db: Session = Depends(get_db)):
    return report_service.current_stock_report(db)


@router.get("/low-stock", response_model=list[LowStockRow], summary="اقلام کم‌موجود (زیر حداقل تعریف‌شده)")
def low_stock(db: Session = Depends(get_db)):
    return report_service.low_stock_report(db)


@router.get("/expiring-batches", response_model=list[ExpiringBatchRow], summary="بچ‌های نزدیک به انقضا")
def expiring_batches(db: Session = Depends(get_db), days_ahead: int = Query(default=30, ge=1, le=365)):
    return report_service.expiring_batches_report(db, days_ahead)


@router.get("/turnover", response_model=list[TurnoverRow], summary="گردش کالا (جمع ورودی/خروجی)")
def turnover(db: Session = Depends(get_db)):
    return report_service.turnover_report(db)
