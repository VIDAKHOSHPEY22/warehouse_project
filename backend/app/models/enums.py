"""
models/enums.py
----------------------------------------------------------------
تمام Enumهای مشترک بین مدل‌ها در یک فایل، تا از پراکندگی و
ناسازگاری مقادیر جلوگیری شود.
----------------------------------------------------------------
"""
import enum


class UserRole(str, enum.Enum):
    """
    نقش‌های سیستم (RBAC ساده):
        ADMIN     -> دسترسی کامل: مدیریت کاربران، اقلام، مکان‌ها، همه گزارش‌ها
        OPERATOR  -> ثبت تخصیص/درخواست، مدیریت مأموریت‌ها، مشاهده گزارش‌ها
        WAREHOUSE -> انباردار: فقط ثبت ورود (Receiving) و خروج (Issue) فیزیکی کالا
    """
    ADMIN = "admin"
    OPERATOR = "operator"
    WAREHOUSE = "warehouse"


class TransactionType(str, enum.Enum):
    """نوع تراکنش انبار - رکن اصلی رهگیری جریان کالا."""
    RECEIPT = "receipt"        # ورود کالا به انبار (از اهداکننده/تأمین‌کننده)
    ISSUE = "issue"            # خروج نهایی کالا از انبار (تحویل به گیرنده/مقصد)
    TRANSFER = "transfer"      # جابجایی بین دو Location داخل همان انبار
    ADJUSTMENT = "adjustment"  # اصلاح موجودی (مثلاً بعد از شمارش فیزیکی/انبارگردانی)
    ALLOCATION = "allocation"  # رزرو/تخصیص به یک مأموریت (کسر از available، نه از موجودی فیزیکی)


class MissionStatus(str, enum.Enum):
    """وضعیت درخواست/مأموریت توزیع."""
    DRAFT = "draft"
    ALLOCATED = "allocated"
    PARTIALLY_DELIVERED = "partially_delivered"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
