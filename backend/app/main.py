"""
main.py
----------------------------------------------------------------
نقطه ورود برنامه FastAPI. مسئولیت‌های این فایل:
    1) ساخت نمونه FastAPI و تنظیم CORS
    2) رجیستر کردن (include) تمام روترها
    3) تعریف یک Health-check ساده برای مانیتورینگ

اجرای توسعه (Development):
    uvicorn app.main:app --reload

اجرای Production (داخل Docker):
    uvicorn app.main:app --host 0.0.0.0 --port 8000
----------------------------------------------------------------
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import auth, users, items, locations, batches, missions, transactions, reports

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=(
        "سامانه مدیریت هوشمند انبار امدادی و توزیع اقلام.\n\n"
        "جریان کاری اصلی: دریافت (Receiving) -> نگهداری (Batch/Location) "
        "-> تخصیص (Allocation) -> تحویل (Issue)."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# رجیستر روترها - هر ماژول مسئول یک بخش از دامنه است (Domain-driven routing)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(locations.router)
app.include_router(batches.router)
app.include_router(missions.router)
app.include_router(transactions.router)
app.include_router(reports.router)


@app.get("/api/health", tags=["سلامت سامانه"], summary="بررسی سلامت سرویس")
def health_check():
    """برای استفاده در Docker healthcheck یا مانیتورینگ بیرونی."""
    return {"status": "ok", "service": settings.PROJECT_NAME, "version": settings.PROJECT_VERSION}
