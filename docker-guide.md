یک قالب کامل و آماده‌کار براتون ساختم، دقیقاً بر اساس فرم مساله‌ای که فرستادید. خلاصه‌ی چیزی که داخل فایل زیپ هست:

**معماری:**
- **Backend**: FastAPI + PostgreSQL + SQLAlchemy، با معماری لایه‌ای (Routes → Services → Models) — منطق کسب‌وکار (تخصیص، خروج، جابجایی) کاملاً در `services/inventory_service.py` جدا شده
- **Frontend**: React + Vite + TailwindCSS، با RTL کامل و فونت وزیرمتن
- **مدل داده**: Item (شناسنامه کالا) جدا از Batch (موجودی واقعی به تفکیک مکان/تاریخ انقضا) — دقیقاً برای پشتیبانی از FEFO و رهگیری دقیق
- **جریان کاری**: دریافت → نگهداری → تخصیص → تحویل، هر مرحله با ثبت خودکار در دفتر کل تراکنش‌ها (Audit Trail)
- **RBAC**: سه نقش (ادمین/کارشناس عملیات/انباردار) با کنترل دسترسی در سطح API
- **Docker**: `docker-compose.yml` کامل برای بالا آوردن همه‌چیز با یک دستور

همه فایل‌ها با کامنت فارسی مستند شدن (چرا این ساختار، چرا این تصمیم طراحی). یک `README.md` جامع هم هست که شامل نمودار معماری، توضیح ERD، راهنمای راه‌اندازی (هم Docker و هم دستی)، مستندات API، و مهم‌تر از همه یک بخش «مراحل بعدی پیشنهادی» که دقیقاً می‌گه از کجا ادامه بدید (بارکد/QR، نمودار گزارش، تست خودکار، و...).

برای شروع سریع:
```bash
cd warehouse-project
cp backend/.env.example backend/.env
docker compose up -d --build
docker compose exec backend python -m app.seed
```
بعدش با `admin` / `Admin@12345` وارد میشید (رمز پیش‌فرض رو حتماً عوض کنید).

 Admin created successfully!
==================================================
🔑 Username: admin
🔑 Password: Admin@Secure2026#
==================================================

اگه بخواید می‌تونم روی بخش خاصی عمیق‌تر بشم — مثلاً تست‌های خودکار pytest براش بنویسم، یا نمودارهای گزارش گرافیکی اضافه کنم، یا بارکد/QR رو پیاده کنم.


 ssh kali@localhost -p 2222


# 🏚️ سامانه مدیریت هوشمند انبار امدادی

## 📋 توضیحات پروژه
این پروژه یک **سیستم مدیریت انبار امدادی** است که برای مدیریت کالاها، مکان‌ها، موجودی، مأموریت‌ها و تراکنش‌های انبار طراحی شده است.

### قابلیت‌های اصلی:
- ✅ مدیریت کالاها (SKU)
- ✅ مدیریت مکان‌های انبار
- ✅ ثبت ورود و خروج کالا
- ✅ انتقال کالا بین مکان‌ها
- ✅ ثبت و مدیریت مأموریت‌ها
- ✅ گزارش‌گیری (موجودی، کم‌موجودی، نزدیک انقضا، گردش کالا)
- ✅ احراز هویت با JWT
- ✅ مدیریت کاربران

---

## 🛠️ پیش‌نیازها
- **Docker** و **Docker Compose** نصب شده باشد.
- **VirtualBox** یا **VMware** برای اجرای ماشین مجازی (اختیاری).
- **VS Code** با افزونه **Remote - SSH** (برای اتصال به VM).

---

## 🚀 نصب و راه‌اندازی

### ۱. اتصال به ماشین مجازی (Kali Linux)
```bash
ssh kali@localhost -p 2222
# پسورد: YourPassword
```

### ۲. نصب Docker روی Kali
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl enable docker --now
sudo usermod -aG docker $USER
# خارج شده و دوباره وارد شوید
exit
ssh kali@localhost -p 2222
```

### ۳. کپی پروژه به VM
```bash
# در PowerShell ویندوز
scp -P 2222 -r E:\warehouse-project kali@localhost:/home/kali/
```

### ۴. اجرای پروژه
```bash
cd ~/warehouse-project
docker compose up -d --build
```

### ۵. بررسی وضعیت کانتینرها
```bash
docker ps
```

---

## 🔑 اطلاعات ورود به سیستم

| فیلد | مقدار |
|------|--------|
| **Username** | `admin` |
| **Password** | `Admin@Secure2026#` |

### دسترسی‌ها:
- **فرانت‌اند**: `http://localhost:3000`
- **بک‌اند (API)**: `http://localhost:8000`
- **مستندات API (Swagger)**: `http://localhost:8000/docs`

---

## 🧪 سناریوهای تست شده

### ۱. ایجاد کالا (Item)
**در فرانت‌اند:**
- 📦 اقلام → افزودن کالای جدید

**از طریق API (Swagger):**
```http
POST /api/items
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "code": "FOOD-001",
  "name": "آرد گندم",
  "category": "مواد غذایی",
  "unit": "کیلوگرم",
  "min_stock": 50,
  "expiry_required": true
}
```

**نمونه دیگر:**
```json
{
  "code": "TEST-001",
  "name": "آزمایشی ۱",
  "category": "مواد مصرفی",
  "unit": "عدد",
  "min_stock": 10,
  "expiry_required": false
}
```

---

### ۲. ایجاد مکان (Location)
**در Swagger:**
```http
POST /api/locations
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "code": "LOC-A1",
  "name": "قفسه A1",
  "zone": "انبار اصلی",
  "description": "قفسه مواد غذایی خشک"
}
```

**مکان‌های ایجاد شده:**
| کد | نام | توضیحات |
|-----|-----|----------|
| LOC-A1 | قفسه A1 | قفسه مواد غذایی خشک |
| LOC-B2 | قفسه B2 | قفسه اقلام مصرفی |
| LOC-C3 | پالت C3 | پالت کالاهای سنگین |

---

### ۳. ثبت ورود کالا (Receiving)
**در فرانت‌اند:**
- ⬇️ ثبت ورود کالا

**از طریق API:**
```http
POST /api/transactions/receive
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "item_id": 1,
  "location_id": 1,
  "quantity": 100,
  "expiry_date": "2027-02-28",
  "source": "اهداکننده: جمعیت هلال احمر",
  "note": "محموله اولیه"
}
```

---

### ۴. ثبت خروج کالا (Issue)
**در فرانت‌اند:**
- ⬆️ ثبت خروج کالا

**از طریق API:**
```http
POST /api/transactions/issue
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "batch_id": 1,
  "quantity": 30,
  "destination": "مناطق سیل‌زده",
  "note": "خروج برای مأموریت امدادی"
}
```

---

### ۵. انتقال کالا بین مکان‌ها (Transfer)
**از طریق API:**
```http
POST /api/transactions/transfer
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "batch_id": 1,
  "to_location_id": 2,
  "quantity": 20,
  "note": "انتقال ۲۰ کیلو آرد از قفسه A1 به B2"
}
```

**برای متمرکز کردن موجودی:**
```json
{
  "batch_id": 3,
  "to_location_id": 1,
  "quantity": 20,
  "note": "انتقال کل موجودی آرد از قفسه B2 به A1"
}
```

---

### ۶. ثبت مأموریت (Mission)
**در فرانت‌اند:**
- 🎯 مأموریت‌ها → ایجاد مأموریت جدید

**از طریق API:**
```http
POST /api/missions
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "code": "M-1404-001",
  "title": "توزیع مواد غذایی در مناطق سیل‌زده",
  "requester": "مدیریت بحران استان",
  "destination": "مناطق سیل‌زده - شهرستان الف",
  "note": "ارسال ۳۰ کیلو آرد برای توزیع"
}
```

---

### ۷. گزارش‌گیری
**در فرانت‌اند:**
- 📈 گزارش‌ها

**از طریق API:**

#### موجودی لحظه‌ای:
```http
GET /api/reports/current-stock
Authorization: Bearer YOUR_TOKEN
```

#### کم‌موجودی:
```http
GET /api/reports/low-stock
Authorization: Bearer YOUR_TOKEN
```

#### نزدیک انقضا:
```http
GET /api/reports/expiring-batches
Authorization: Bearer YOUR_TOKEN
```

#### گردش کالا:
```http
GET /api/reports/turnover
Authorization: Bearer YOUR_TOKEN
```

---

## 📊 وضعیت نهایی تست‌ها

| # | سناریو | وضعیت | توضیحات |
|---|--------|--------|----------|
| ۱ | ایجاد کالا | ✅ موفق | ۲ کالا ایجاد شد |
| ۲ | ایجاد مکان | ✅ موفق | ۳ مکان ایجاد شد |
| ۳ | ثبت ورود کالا | ✅ موفق | آرد گندم: ۱۰۰ کیلو، آزمایشی ۱: ۵۰ عدد |
| ۴ | ثبت خروج کالا | ✅ موفق | خروج ۳۰ کیلو آرد |
| ۵ | انتقال کالا | ✅ موفق | انتقال ۲۰ کیلو از A1 به B2 |
| ۶ | متمرکز کردن موجودی | ✅ موفق | کل آرد در قفسه A1: ۵۰ کیلو |
| ۷ | ثبت مأموریت | ✅ موفق | M-1404-001 |
| ۸ | گزارش موجودی لحظه‌ای | ✅ موفق | نمایش دقیق موجودی |
| ۹ | گزارش کم‌موجودی | ✅ موفق | آزمایشی ۱: ۵ < ۱۰ |
| ۱۰ | احراز هویت (JWT) | ✅ موفق | توکن معتبر |

---

## 📝 نکات مدیریتی مهم

### ۱. موجودی کل بررسی می‌شود
سیستم **موجودی کل** کالا رو در همه مکان‌ها جمع می‌زنه و با `min_stock` مقایسه میکنه.

**مثال:**
- آرد گندم در ۲ مکان: A1=30, B2=20 → مجموع=50
- حداقل مجاز=50 → ✅ نرمال

### ۲. متمرکز کردن موجودی
برای مدیریت بهتر، موجودی هر کالا رو در یک مکان متمرکز کنید.

### ۳. بچ‌های خالی
بچ‌های با موجودی صفر به طور خودکار حذف نمی‌شوند. می‌توانید آنها را غیرفعال کنید.

---

## 🛠️ دستورات مفید

### مشاهده لاگ‌ها:
```bash
docker compose logs backend --tail 50
docker compose logs frontend --tail 50
docker compose logs db --tail 30
```

### ریستارت سرویس‌ها:
```bash
docker compose restart backend
docker compose restart frontend
docker compose restart db
```

### توقف و حذف کانتینرها:
```bash
docker compose down
```

### بازسازی و اجرا:
```bash
docker compose up -d --build
```

### ورود به کانتینر بک‌اند:
```bash
docker exec -it warehouse-project-backend-1 bash
```

### ایجاد کاربر ادمین (اگر نیاز شد):
```bash
docker exec -it warehouse-project-backend-1 python -c "
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password
db = SessionLocal()
admin = db.query(User).filter(User.username == 'admin').first()
if admin:
    admin.hashed_password = hash_password('Admin@Secure2026#')
    db.commit()
    print('✅ Password updated!')
else:
    admin = User(username='admin', hashed_password=hash_password('Admin@Secure2026#'), full_name='مدیر سیستم', role='admin', is_active=True)
    db.add(admin)
    db.commit()
    print('✅ Admin created!')
db.close()
"
```

---

## ⚠️ عیب‌یابی

### ۱. خطای 401 (Unauthorized)
توکن منقضی شده است. دوباره لاگین کنید:
```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=Admin@Secure2026#
```

### ۲. خطای 500 (Internal Server Error)
لاگ بک‌اند را بررسی کنید:
```bash
docker compose logs backend --tail 50
```

### ۳. اتصال به دیتابیس
بررسی سلامت دیتابیس:
```bash
docker compose exec db psql -U warehouse_user -d warehouse_db -c "SELECT 1;"
```

### ۴. پورت‌ها در دسترس نیستند
مطمئن شوید Port Forwarding در VirtualBox تنظیم شده است:
- SSH: 127.0.0.1:2222 → 10.0.2.15:22
- Frontend: 127.0.0.1:3000 → 10.0.2.15:80
- Backend: 127.0.0.1:8000 → 10.0.2.15:8000

---

## 📚 منابع مفید

- **مستندات API**: `http://localhost:8000/docs`
- **فرانت‌اند**: `http://localhost:3000`
- **Docker**: [https://docs.docker.com/](https://docs.docker.com/)
- **FastAPI**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

---

## ✅ نتیجه‌گیری نهایی

سیستم **سامانه مدیریت هوشمند انبار امدادی** با موفقیت نصب، پیکربندی و تست شد. 
همه سناریوهای اصلی (ورود، خروج، انتقال، مأموریت، گزارش‌گیری) با موفقیت انجام شدند.

### تاریخ تست: ۲۸ امرداد ۱۴۰۵ (۲۸ آگوست ۲۰۲۶)
### وضعیت نهایی: ✅ **عملیاتی و پایدار**


## 📋 راهنمای کامل برای بازگشت به پروژه بعد از خاموش کردن لپ‌تاپ

### 🟢 مرحله ۱: روشن کردن ماشین مجازی (VM)

1. **VirtualBox** رو باز کنید.
2. روی ماشین مجازی **Kali** کلیک کنید.
3. دکمه **Start** (سبز رنگ) رو بزنید.
4. صبر کنید تا Kali کامل بالا بیاد (تا صفحه لاگین یا دسکتاپ).

---

### 🟢 مرحله ۲: اتصال به VM از طریق VS Code

#### روش ۱: از طریق Command Palette (سریع‌ترین)

1. **VS Code** رو باز کنید.
2. کلیدهای `F1` یا `Ctrl+Shift+P` رو بزنید.
3. تایپ کنید: `Remote-SSH: Connect to Host...`
4. از لیست، **`kali-vm`** رو انتخاب کنید.
5. پسورد کاربر `kali` رو وارد کنید.

#### روش ۲: از طریق تنظیمات SSH

1. VS Code رو باز کنید.
2. کلیدهای `F1` رو بزنید.
3. تایپ کنید: `Remote-SSH: Connect to Host...`
4. آدرس کامل رو وارد کنید: `kali@localhost -p 2222`
5. پسورد رو وارد کنید.

---

### 🟢 مرحله ۳: باز کردن پوشه پروژه

بعد از اتصال:

1. از منوی **File** → **Open Folder** برید.
2. آدرس رو وارد کنید:
   ```
   /home/kali/warehouse-project
   ```
3. روی **OK** کلیک کنید.

---

### 🟢 مرحله ۴: اجرای کانتینرها (Docker)

1. ترمینال VS Code رو باز کنید (`Ctrl + `` `).
2. دستورات زیر رو به ترتیب اجرا کنید:

```bash
cd ~/warehouse-project
docker compose up -d
docker ps
```

---

### 🟢 مرحله ۵: دسترسی به سیستم

حالا می‌تونید از مرورگر ویندوز به آدرس‌های زیر برید:

- **فرانت‌اند**: `http://localhost:3000`
- **بک‌اند (API)**: `http://localhost:8000`
- **مستندات API (Swagger)**: `http://localhost:8000/docs`

**اطلاعات ورود:**
- **Username**: `admin`
- **Password**: `Admin@Secure2026#`

---

## 📌 خلاصه دستورات (برای کپی سریع):

```bash
# بعد از اتصال VS Code به VM
cd ~/warehouse-project
docker compose up -d
docker ps

# اگر خطای docker not found داد:
sudo systemctl start docker
sudo systemctl enable docker
```

---

## ✅ نکات مهم:

| کار | دستور / راهنما |
|-----|----------------|
| **اتصال SSH** | `ssh kali@localhost -p 2222` (اگر VS Code وصل نشد) |
| **مشاهده لاگ کانتینرها** | `docker compose logs --tail 50` |
| **ریستارت کانتینرها** | `docker compose restart` |
| **توقف کانتینرها** | `docker compose down` |
| **مشاهده وضعیت کانتینرها** | `docker ps` |

---

## 🛑 قبل از خاموش کردن لپ‌تاپ (اختیاری):

> **توجه:** لازم نیست کانتینرها رو متوقف کنید. وقتی لپ‌تاپ رو خاموش می‌کنید، کانتینرها خودکار متوقف می‌شن و دفعه بعد با `docker compose up -d` دوباره اجرا می‌شن.

ولی اگر می‌خواید خودتون متوقفشون کنید:

```bash
cd ~/warehouse-project
docker compose down
```

---

**حالا می‌تونید با خیال راحت لپ‌تاپ رو خاموش کنید و دفعه بعد با این راهنما دوباره شروع کنید.** 🚀