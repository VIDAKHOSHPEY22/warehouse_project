"""
core/config.py
----------------------------------------------------------------
تنظیمات سراسری برنامه.
تمام مقادیر حساس (رمز دیتابیس، کلید JWT و ...) از فایل .env خوانده
می‌شوند تا هرگز داخل کد commit نشوند.

نحوه استفاده در جاهای دیگر پروژه:
    from app.core.config import settings
    settings.DATABASE_URL
----------------------------------------------------------------
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # آدرس اتصال به دیتابیس
    DATABASE_URL: str = "postgresql+psycopg2://warehouse_user:warehouse_pass@localhost:5432/warehouse_db"

    # تنظیمات امنیتی JWT
    SECRET_KEY: str = "CHANGE_ME"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 ساعت - معادل یک شیفت کاری

    # کاربر ادمین اولیه (برای اسکریپت seed)
    FIRST_ADMIN_USERNAME: str = "admin"
    FIRST_ADMIN_PASSWORD: str = "Admin@12345"
    FIRST_ADMIN_FULLNAME: str = "مدیر سیستم"

    # لیست دامنه‌های مجاز برای CORS (جدا شده با کاما)
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    PROJECT_NAME: str = "سامانه مدیریت هوشمند انبار امدادی"
    PROJECT_VERSION: str = "1.0.0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
