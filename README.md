# نظام تنظيم المرضى للعيادات - Clinic Queue Manager

نظام ويب لتنظيم دخول المرضى للعيادات، مرتبط بقاعدة بيانات SQL Server.

## المميزات

- إعداد اتصال قاعدة البيانات عند التشغيل الأول
- عرض المرضى في الانتظار في جدول منظم
- تأكيد دخول المريض للطبيب بضغطة زر
- تحديث تلقائي للجدول كل 10 ثوانٍ
- واجهة عربية بتصميم RTL

## المتطلبات

- Python 3.10+
- SQL Server (على الشبكة المحلية)
- ODBC Driver 17 for SQL Server

## التثبيت والتشغيل

```bash
# تثبيت المتطلبات
pip install -e .

# أو باستخدام uv
uv pip install -e .

# تشغيل التطبيق
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

ثم افتح المتصفح على `http://localhost:8000`

## إعداد قاعدة البيانات

عند التشغيل الأول، ستظهر صفحة إعداد لإدخال:
- اسم السيرفر (Server Name)
- اسم المستخدم (Username)
- كلمة المرور (Password)

قاعدة البيانات: `hospimag`

## جدول البيانات

| العمود | النوع | الوصف |
|--------|-------|-------|
| Tktno | string | رقم التذكرة |
| Pname | string | اسم المريض |
| Drname | string | اسم الطبيب |
| Countertime | datetime | وقت الكاونتر |
| Drentertime | datetime | وقت دخول الطبيب |
| Labrequesttime | datetime | وقت طلب المعمل |
| Servicerequesttime | datetime | وقت طلب الخدمة |
| Status | string | الحالة |
| Usr | string | المستخدم |
| Dt | date | التاريخ |
