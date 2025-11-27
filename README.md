# 🎓 سیستم مدیریت مدرسه و یادگیری آنلاین
## School Management & E-Learning System

یک سیستم جامع مدیریت مدرسه و یادگیری آنلاین با رابط کاربری پیشرفته و افکت‌های شیشه‌ای Aero Glass

A comprehensive school management and e-learning system with advanced UI featuring Aero Glass effects and hue color shifting animations.

---

## ✨ ویژگی‌ها / Features

### 🔐 سیستم احراز هویت / Authentication System
- ورود امن با نام کاربری و رمز عبور / Secure login with username and password
- سه نقش کاربری: مدیر، معلم، دانش‌آموز / Three user roles: Admin, Teacher, Student

### 👨‍💼 پنل مدیریت / Admin Panel
- ✅ افزودن، حذف و ویرایش دانش‌آموزان / Add, remove, and edit students
- ✅ افزودن، حذف و ویرایش معلمان / Add, remove, and edit teachers
- ✅ مشاهده تمام کلاس‌ها / View all classes
- ✅ آمار و گزارش‌گیری / Statistics and reporting

### 👨‍🏫 پنل معلم / Teacher Panel
- 📚 ایجاد و مدیریت کلاس‌های آنلاین / Create and manage online classes
- 🎥 اشتراک‌گذاری ویدیو و صدا (WebRTC) / Video and audio sharing (WebRTC)
- 📎 آپلود منابع و فایل‌های درسی / Upload class materials and files
- ✅ بررسی و نمره‌دهی به تکالیف دانش‌آموزان / Review and grade student homework
- 💬 ارائه بازخورد به دانش‌آموزان / Provide feedback to students

### 👨‍🎓 پنل دانش‌آموز / Student Panel
- 📚 ثبت‌نام در کلاس‌ها / Enroll in classes
- 🎥 شرکت در کلاس‌های آنلاین / Participate in online classes
- 📝 ارسال تکالیف / Submit homework
- 📥 دانلود منابع درسی / Download class materials
- 📊 مشاهده نمرات و بازخورد معلمان / View grades and teacher feedback

### 🎨 طراحی UI پیشرفته / Advanced UI Design
- ✨ افکت‌های Aero Glass / Aero Glass effects
- 🌈 انیمیشن‌های تغییر رنگ Hue / Hue color shifting animations
- 📱 طراحی ریسپانسیو / Responsive design
- 🇮🇷 رابط کاربری فارسی / Persian language interface
- 🎭 انیمیشن‌های روان / Smooth animations

---

## 🚀 نصب و راه‌اندازی / Installation & Setup

### پیش‌نیازها / Prerequisites
- Python 3.8 یا بالاتر / Python 3.8 or higher
- مرورگر مدرن (Chrome، Firefox، Edge) / Modern web browser

### مراحل نصب / Installation Steps

#### 1️⃣ نصب وابستگی‌ها / Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2️⃣ اجرای برنامه / Run the Application
```bash
python school_app.py
```

#### 3️⃣ دسترسی به سیستم / Access the System
مرورگر خود را باز کرده و به آدرس زیر بروید:
Open your browser and go to:
```
http://localhost:5000
```

---

## 🔑 اطلاعات ورود پیش‌فرض / Default Login Credentials

### مدیر سیستم / System Administrator
- **نام کاربری / Username:** `admin`
- **رمز عبور / Password:** `admin123`

> ⚠️ **نکته امنیتی:** پس از اولین ورود، حتماً رمز عبور را تغییر دهید
> 
> **Security Note:** Change the password after first login

---

## 📁 ساختار پروژه / Project Structure

```
school-management-system/
│
├── school_app.py           # فایل اصلی برنامه / Main application file
├── school.db               # پایگاه داده SQLite (ساخته می‌شود) / SQLite database (auto-created)
├── requirements.txt        # وابستگی‌های Python / Python dependencies
│
├── templates/              # قالب‌های HTML / HTML templates
│   ├── base.html          # قالب پایه / Base template
│   ├── login.html         # صفحه ورود / Login page
│   ├── admin_dashboard.html    # داشبورد مدیر / Admin dashboard
│   ├── teacher_dashboard.html  # داشبورد معلم / Teacher dashboard
│   ├── teacher_class.html      # صفحه کلاس معلم / Teacher class page
│   ├── student_dashboard.html  # داشبورد دانش‌آموز / Student dashboard
│   └── student_class.html      # صفحه کلاس دانش‌آموز / Student class page
│
├── static/                 # فایل‌های استاتیک / Static files
│   ├── css/
│   │   └── style.css      # استایل‌ها / Styles
│   └── js/
│       └── script.js      # جاوااسکریپت / JavaScript
│
└── uploads/               # فایل‌های آپلود شده (ساخته می‌شود) / Uploaded files (auto-created)
    ├── homework/          # تکالیف دانش‌آموزان / Student homework
    └── materials/         # منابع درسی / Class materials
```

---

## 🎯 راهنمای استفاده / Usage Guide

### برای مدیر سیستم / For Administrators

1. با حساب مدیر وارد شوید / Login with admin account
2. از داشبورد مدیر می‌توانید:
   - دانش‌آموزان جدید اضافه کنید / Add new students
   - معلمان جدید اضافه کنید / Add new teachers
   - کاربران را ویرایش یا حذف کنید / Edit or delete users
   - آمار کلی سیستم را مشاهده کنید / View system statistics

### برای معلمان / For Teachers

1. با حساب معلم وارد شوید / Login with teacher account
2. کلاس جدید ایجاد کنید / Create a new class
3. لینک جلسه آنلاین اضافه کنید / Add online meeting link
4. منابع درسی آپلود کنید / Upload class materials
5. تکالیف دانش‌آموزان را بررسی و نمره‌دهی کنید / Review and grade student homework

### برای دانش‌آموزان / For Students

1. با حساب دانش‌آموز وارد شوید / Login with student account
2. در کلاس‌های مورد نظر ثبت‌نام کنید / Enroll in desired classes
3. در جلسات آنلاین شرکت کنید / Join online sessions
4. منابع درسی را دانلود کنید / Download class materials
5. تکالیف خود را ارسال کنید / Submit your homework
6. نمرات و بازخورد معلمان را مشاهده کنید / View grades and feedback

---

## 🎥 ویژگی‌های ویدئو کنفرانس / Video Conferencing Features

### دو روش برای برگزاری کلاس آنلاین:

#### 1️⃣ استفاده از لینک خارجی / Using External Links
- Google Meet
- Zoom
- Microsoft Teams
- Jitsi Meet
- و سایر سرویس‌ها / And other services

#### 2️⃣ استفاده از WebRTC داخلی / Using Built-in WebRTC
- دسترسی مستقیم به دوربین و میکروفون / Direct camera and microphone access
- کنترل دوربین و میکروفون / Camera and microphone controls
- بدون نیاز به نرم‌افزار خارجی / No external software needed

---

## 🛠️ تنظیمات پیشرفته / Advanced Configuration

### تغییر پورت سرور / Change Server Port
در فایل `school_app.py` خط آخر را تغییر دهید:
Modify the last line in `school_app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5000)  # پورت را تغییر دهید / Change port here
```

### افزایش حداکثر حجم فایل آپلود / Increase Upload File Size
در فایل `school_app.py`:

```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

---

## 🔒 نکات امنیتی / Security Notes

1. **رمز عبور پیش‌فرض را تغییر دهید** / Change default passwords
2. **در محیط production از HTTPS استفاده کنید** / Use HTTPS in production
3. **Secret Key را تغییر دهید** / Change the secret key
4. **پشتیبان منظم از دیتابیس بگیرید** / Regular database backups

---

## 📱 سازگاری مرورگرها / Browser Compatibility

✅ Chrome 90+
✅ Firefox 88+
✅ Edge 90+
✅ Safari 14+
✅ Opera 76+

---

## 🐛 عیب‌یابی / Troubleshooting

### مشکل در دسترسی به دوربین/میکروفون / Camera/Microphone Access Issues
- مجوزهای مرورگر را بررسی کنید / Check browser permissions
- از HTTPS استفاده کنید یا localhost / Use HTTPS or localhost
- مرورگر را ری‌استارت کنید / Restart your browser

### خطای پایگاه داده / Database Errors
```bash
# حذف دیتابیس و ساخت مجدد / Delete database and recreate
rm school.db
python school_app.py
```

### مشکل در نمایش فونت فارسی / Persian Font Display Issues
- اتصال اینترنت را بررسی کنید (برای دانلود فونت Vazirmatn)
- Check internet connection (for downloading Vazirmatn font)

---

## 🎨 سفارشی‌سازی ظاهر / Customizing Appearance

### تغییر رنگ‌های اصلی / Changing Main Colors
فایل `static/css/style.css` را ویرایش کنید:
Edit `static/css/style.css`:

```css
.animated-background {
    background: linear-gradient(45deg, 
        hsl(180, 70%, 50%),  /* رنگ اول / First color */
        hsl(240, 70%, 50%),  /* رنگ دوم / Second color */
        hsl(300, 70%, 50%),  /* رنگ سوم / Third color */
        hsl(360, 70%, 50%)); /* رنگ چهارم / Fourth color */
}
```

---

## 📊 پایگاه داده / Database Schema

سیستم از SQLite استفاده می‌کند با جداول زیر:
The system uses SQLite with the following tables:

- **users** - کاربران (مدیر، معلم، دانش‌آموز) / Users (admin, teacher, student)
- **classes** - کلاس‌ها / Classes
- **homework** - تکالیف / Homework submissions
- **enrollments** - ثبت‌نام‌ها / Class enrollments
- **class_materials** - منابع درسی / Class materials

---

## 🤝 مشارکت / Contributing

این پروژه متن‌باز است و از مشارکت شما استقبال می‌کنیم!
This project is open-source and we welcome your contributions!

---

## 📝 مجوز / License

این پروژه تحت مجوز MIT منتشر شده است.
This project is released under the MIT License.

---

## 💡 نکات مهم / Important Notes

1. ⚠️ این سیستم برای استفاده آموزشی و در محیط‌های محلی طراحی شده است
   This system is designed for educational purposes and local environments

2. 🔐 برای استفاده در محیط production، لطفاً اقدامات امنیتی اضافی اعمال کنید
   For production use, please implement additional security measures

3. 💾 پایگاه داده SQLite برای پروژه‌های کوچک مناسب است
   SQLite database is suitable for small projects

4. 🎥 برای ویدیوکنفرانس پیشرفته‌تر، توصیه می‌شود از سرویس‌های حرفه‌ای استفاده کنید
   For advanced video conferencing, we recommend using professional services

---

## 📞 پشتیبانی / Support

در صورت بروز مشکل یا سوال، لطفاً یک Issue در GitHub ایجاد کنید.
If you encounter any issues or have questions, please create an Issue on GitHub.

---

## 🎓 ساخته شده با / Built With

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite
- **UI Framework:** Custom Aero Glass CSS
- **Font:** Vazirmatn (Persian)
- **Video:** WebRTC

---

**🌟 از استفاده از این سیستم لذت ببرید! / Enjoy using this system! 🌟**
