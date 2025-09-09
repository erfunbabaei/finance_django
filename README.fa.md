
---

### **4️⃣ فایل `README.fa.md` (فارسی)**

```markdown
# پروژه Django مدیریت مالی

این پروژه یک بک‌اند بر پایه Django برای مدیریت مالی شخصی است.

## امکانات

- احراز هویت JWT با توکن‌های Access و Refresh در کوکی‌ها
- ثبت نام و ورود کاربران
- مدیریت درآمد و هزینه‌ها
- API خلاصه‌سازی داشبورد
- Endpoint های RESTful برای عملیات CRUD
- آماده برای اتصال به فرانت‌اند با CORS

## نصب و راه‌اندازی

1. کلون کردن مخزن:
```bash
git clone <your-repo-link>

نصب پکیج‌ها:
pip install -r requirements.txt

پیکربندی فایل .env برای تنظیمات دیتابیس و کلیدهای مخفی.

اعمال مهاجرت‌ها:
python manage.py migrate

اجرای سرور:
python manage.py runserver

API Endpoints

POST /api/register/ - ثبت نام کاربر جدید

POST /api/login/ - ورود و دریافت کوکی‌های JWT

GET /api/logout/ - خروج و حذف کوکی‌ها

GET /api/dashboard/ - دریافت خلاصه درآمد و هزینه‌ها

CRUD /api/incomes/ - مدیریت درآمدها

CRUD /api/expenses/ - مدیریت هزینه‌ها

