"""
core/database.py
----------------------------------------------------------------
راه‌اندازی اتصال SQLAlchemy به PostgreSQL.

الگوی طراحی:
    - engine: یک نمونه واحد که Connection Pool را مدیریت می‌کند.
    - SessionLocal: کارخانه ساخت Session برای هر درخواست HTTP.
    - get_db(): یک Dependency برای FastAPI که Session می‌سازد و در
      پایان درخواست آن را می‌بندد (الگوی Unit of Work).
    - Base: کلاس پایه‌ای که همه مدل‌های ORM از آن ارث‌بری می‌کنند.
----------------------------------------------------------------
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# pool_pre_ping=True: قبل از هر استفاده از کانکشن، سلامت آن را تست می‌کند
# تا از خطای "connection closed" بعد از بی‌کاری طولانی جلوگیری شود.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()


def get_db():
    """
    Dependency استاندارد FastAPI برای تزریق Session دیتابیس به هر Endpoint.
    استفاده:
        @router.get("/items")
        def list_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
