"""
seed.py
----------------------------------------------------------------
اسکریپت مقداردهی اولیه دیتابیس:
    1) ساخت جدول‌ها (در محیط توسعه - در Production از Alembic استفاده کنید)
    2) ساخت کاربر ادمین اولیه
    3) چند مکان و کالای نمونه برای شروع کار سریع

اجرا:
    python -m app.seed
یا داخل کانتینر:
    docker compose exec backend python -m app.seed
----------------------------------------------------------------
"""
from app.core.database import Base, engine, SessionLocal
from app.core.security import hash_password
from app.core.config import settings
from app.models.user import User
from app.models.location import Location
from app.models.item import Item
from app.models.enums import UserRole


def run():
    print("در حال ساخت جدول‌ها...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # --- کاربر ادمین ---
        if not db.query(User).filter(User.username == settings.FIRST_ADMIN_USERNAME).first():
            admin = User(
                username=settings.FIRST_ADMIN_USERNAME,
                full_name=settings.FIRST_ADMIN_FULLNAME,
                hashed_password=hash_password(settings.FIRST_ADMIN_PASSWORD),
                role=UserRole.ADMIN,
                is_active=True,
            )
            db.add(admin)
            print(f"کاربر ادمین ساخته شد -> username: {settings.FIRST_ADMIN_USERNAME}")
        else:
            print("کاربر ادمین از قبل وجود دارد.")

        # --- کاربران نمونه دیگر ---
        sample_users = [
            ("operator1", "کارشناس عملیات", UserRole.OPERATOR, "Operator@123"),
            ("warehouse1", "انباردار اول", UserRole.WAREHOUSE, "Warehouse@123"),
        ]
        for username, full_name, role, password in sample_users:
            if not db.query(User).filter(User.username == username).first():
                db.add(User(username=username, full_name=full_name, role=role,
                             hashed_password=hash_password(password), is_active=True))

        # --- مکان‌های نمونه ---
        sample_locations = [
            ("A1", "قفسه غذایی - ردیف ۱"),
            ("A2", "قفسه غذایی - ردیف ۲"),
            ("B1", "قفسه پوشاک - ردیف ۱"),
            ("C1", "قفسه بهداشتی - ردیف ۱"),
        ]
        for code, name in sample_locations:
            if not db.query(Location).filter(Location.code == code).first():
                db.add(Location(code=code, name=name))

        # --- کالاهای نمونه ---
        sample_items = [
            ("FOOD-001", "کنسرو لوبیا", "غذا", "قوطی", True, 50),
            ("FOOD-002", "آب معدنی ۱.۵ لیتری", "غذا", "بطری", False, 200),
            ("HYG-001", "پک بهداشتی خانوار", "بهداشت", "بسته", False, 30),
            ("CLOTH-001", "پتوی گرم", "پوشاک", "عدد", False, 20),
        ]
        for code, name, category, unit, expiry_required, min_stock in sample_items:
            if not db.query(Item).filter(Item.code == code).first():
                db.add(Item(code=code, name=name, category=category, unit=unit,
                             expiry_required=expiry_required, min_stock=min_stock))

        db.commit()
        print("داده‌های اولیه با موفقیت ثبت شدند.")
        print("-" * 50)
        print(f"ورود ادمین -> username: {settings.FIRST_ADMIN_USERNAME} | password: {settings.FIRST_ADMIN_PASSWORD}")
        print("-" * 50)
    finally:
        db.close()


if __name__ == "__main__":
    run()
