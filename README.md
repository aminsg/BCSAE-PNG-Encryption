<div dir="ltr">

# BCSAE Color PNG Encryption

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License"/>
  <img src="https://img.shields.io/badge/Encryption-BCSAE-orange" alt="BCSAE"/>
  <img src="https://img.shields.io/badge/Format-PNG%20Lossless-purple" alt="PNG Lossless"/>
</p>

<p align="center">
  <a href="#english-documentation">🇬🇧 English</a> &nbsp;|&nbsp;
  <a href="#مستندات-فارسی">🇮🇷 فارسی</a>
</p>

---

## English Documentation

**BCSAE Color PNG Encryption** is a Python tool that encrypts any binary file and stores it as a lossless PNG image. The encrypted file is visually unrecognizable, carries the original filename inside the encrypted payload, and can be perfectly restored to its original state.

### ✨ Features

- **Lossless PNG output** – Binary files are recovered byte-for-byte, with zero data loss
- **BCSAE algorithm** – Multi-layer encryption: bit inversion, Caesar shifts, and XOR keystream derived from a passphrase using SHA-256
- **zlib compression** – Payload is compressed at level 9 before encoding
- **Original filename preserved** – The original name and extension are stored inside the encrypted header
- **Progress bars** – Real-time progress display via `tqdm`
- **CLI interface** – Simple command-line usage for both encryption and decryption

---

### 📋 Requirements

| Package | Version | Purpose |
|---------|---------|---------|
| Python  | 3.8+    | Runtime |
| Pillow  | Any     | PNG image I/O |
| tqdm    | Any     | Progress bars (optional but recommended) |

---

### ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/aminsg/bcsae-png-encryption.git
cd bcsae-png-encryption
```

**2. (Recommended) Create a virtual environment**
```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install Pillow tqdm
```

> ⚠️ `tqdm` is optional. If not installed, the tool will still work but without progress bars.

---

### 🚀 Usage

#### Basic Syntax
```
python bcsae.py <mode> <input_file> [--pass PASSPHRASE] [--outdir OUTPUT_DIR]
```

| Argument | Description |
|----------|-------------|
| `mode`   | `e` for encrypt, `d` for decrypt |
| `input`  | Path to the input file (any file for encrypt, `.png` for decrypt) |
| `--pass` | Passphrase (optional – you will be prompted securely if omitted) |
| `--outdir` | Output directory for the decrypted file (optional) |

---

### 📖 Examples

#### Encrypt a file
```bash
# Will prompt for passphrase securely
python bcsae.py e secret_document.pdf

# With passphrase provided directly
python bcsae.py e secret_document.pdf --pass "MyStr0ngP@ssword"

# Encrypt any binary file (images, zips, executables, etc.)
python bcsae.py e photo.jpg --pass "hunter2"
python bcsae.py e archive.zip --pass "hunter2"
python bcsae.py e program.exe --pass "hunter2"
```
✅ Output: `secret_document.png` (saved next to the original file)

---

#### Decrypt a file
```bash
# Will prompt for passphrase securely
python bcsae.py d secret_document.png

# With passphrase provided directly
python bcsae.py d secret_document.png --pass "MyStr0ngP@ssword"

# Decrypt to a specific output directory
python bcsae.py d secret_document.png --pass "MyStr0ngP@ssword" --outdir /home/user/recovered/

# Decrypt on Windows
python bcsae.py d secret_document.png --pass "MyStr0ngP@ssword" --outdir C:\Users\User\Desktop\
```
✅ Output: `secret_document.pdf` (original filename and extension are automatically restored)

---

#### Full example – encrypt then decrypt
```bash
# Step 1: Encrypt
python bcsae.py e report.docx --pass "correct-horse-battery-staple"
# Output: report.png

# Step 2: Transfer report.png securely to another machine

# Step 3: Decrypt
python bcsae.py d report.png --pass "correct-horse-battery-staple"
# Output: report.docx  (identical to the original)
```

---

### 🔐 How the Encryption Works

The BCSAE algorithm applies the following operations in sequence:

```
Original data
    │
    ▼
① Invert all bits (XOR with 0xFF)
    │
    ▼
② Caesar shift +3 (each byte += 3 mod 256)
    │
    ▼
③ Invert all bits again
    │
    ▼
④ Caesar shift +1 (each byte += 1 mod 256)
    │
    ▼
⑤ XOR with keystream (SHA-256 derived from passphrase + random 16-byte salt)
    │
    ▼
⑥ Compress with zlib (level 9)
    │
    ▼
Final payload stored in PNG
```

**Stored inside the PNG:**
```
[16-byte salt] [2-byte filename length] [filename bytes] [encrypted+compressed payload]
```

> The salt is randomly generated for each encryption, meaning encrypting the same file twice produces two entirely different PNG images.

---

### ⚠️ Important Notes

> 🔑 **There is no key recovery.** If you forget your passphrase, the data cannot be decrypted. Store your passphrase securely.

> 📦 **The output is always a PNG.** Even if the input is already an image, the output PNG will look like random noise.

> 💾 **Do not re-compress or re-encode the PNG.** Any lossy operation (JPEG conversion, screenshot, image editing with lossy export) will permanently corrupt the encrypted data. Always keep the PNG lossless.

> 🧩 **Padding bytes** – The conversion to pixels requires data length to be a multiple of 3. A small number of null bytes (`0x00`) are added as padding and are automatically stripped during decryption.

> ⏱ **Performance** – Large files may take a while. The progress bar shows encryption/decryption progress in real time.

---

### 📂 Project Structure

```
bcsae-png-encryption/
│
├── bcsae.py          # Main script (encryption + decryption)
├── README.md         # This file
└── requirements.txt  # Python dependencies
```

---

### 📄 License

This project is licensed under the **MIT License** – feel free to use, modify, and distribute it.

---

---

</div>

---

<div dir="rtl">

## مستندات فارسی

**BCSAE Color PNG Encryption** یک ابزار پایتونی است که هر فایل باینری را رمزگذاری کرده و به صورت یک تصویر PNG بدون افت کیفیت (lossless) ذخیره می‌کند. فایل خروجی ظاهراً تصویر بی‌معنایی است، اما نام و پسوند فایل اصلی درون payload رمزشده نگه‌داری می‌شود و فایل می‌تواند بدون هیچ تغییری بازیابی شود.

### ✨ ویژگی‌ها

- **خروجی PNG بدون افت** – فایل‌های باینری به طور کامل و بدون تغییر یک بایت بازگردانده می‌شوند
- **الگوریتم BCSAE** – رمزگذاری چندلایه: معکوس‌سازی بیت، جابجایی سزار، و XOR با keystream برگرفته از رمز عبور با SHA-256
- **فشرده‌سازی zlib** – payload قبل از رمزگذاری با سطح ۹ فشرده می‌شود
- **حفظ نام فایل اصلی** – نام و پسوند اصلی درون header رمزشده ذخیره می‌شود
- **نوار پیشرفت** – نمایش پیشرفت لحظه‌ای با `tqdm`
- **رابط خط فرمان (CLI)** – استفاده ساده از طریق ترمینال

---

### 📋 پیش‌نیازها

| پکیج   | نسخه    | کاربرد |
|--------|---------|--------|
| Python | 3.8+    | اجرای برنامه |
| Pillow | هر نسخه | خواندن و نوشتن PNG |
| tqdm   | هر نسخه | نوار پیشرفت (اختیاری اما توصیه شده) |

---

### ⚙️ نصب

**۱. دریافت مخزن**
```bash
git clone https://github.com/aminsg/bcsae-png-encryption.git
cd bcsae-png-encryption
```

**۲. (پیشنهادی) ساختن محیط مجازی**
```bash
python -m venv venv

# لینوکس / مک
source venv/bin/activate

# ویندوز
venv\Scripts\activate
```

**۳. نصب وابستگی‌ها**
```bash
pip install Pillow tqdm
```

> ⚠️ نصب `tqdm` اختیاری است. در صورت نبود آن، برنامه بدون نوار پیشرفت اجرا می‌شود.

---

### 🚀 نحوه استفاده

#### ساختار دستور

<div dir="ltr">

```
python bcsae.py <mode> <input_file> [--pass PASSPHRASE] [--outdir OUTPUT_DIR]
```

</div>

| آرگومان     | توضیح |
|------------|-------|
| `mode`     | `e` برای رمزگذاری، `d` برای رمزگشایی |
| `input`    | مسیر فایل ورودی (هر فایلی برای رمزگذاری، فایل `.png` برای رمزگشایی) |
| `--pass`   | رمز عبور (اختیاری – اگر وارد نشود، به صورت امن پرسیده می‌شود) |
| `--outdir` | پوشه خروجی فایل رمزگشایی شده (اختیاری) |

---

### 📖 مثال‌ها

#### رمزگذاری فایل

<div dir="ltr">

```bash
# بدون رمز عبور – به صورت امن پرسیده می‌شود
python bcsae.py e document_secret.pdf

# با رمز عبور مستقیم
python bcsae.py e document_secret.pdf --pass "MyStr0ngP@ssword"

# رمزگذاری انواع مختلف فایل
python bcsae.py e photo.jpg --pass "hunter2"
python bcsae.py e archive.zip --pass "hunter2"
python bcsae.py e program.exe --pass "hunter2"
```

</div>

✅ خروجی: `document_secret.png` (کنار فایل اصلی ذخیره می‌شود)

---

#### رمزگشایی فایل

<div dir="ltr">

```bash
# بدون رمز عبور – به صورت امن پرسیده می‌شود
python bcsae.py d document_secret.png

# با رمز عبور مستقیم
python bcsae.py d document_secret.png --pass "MyStr0ngP@ssword"

# رمزگشایی در پوشه مشخص (لینوکس)
python bcsae.py d document_secret.png --pass "MyStr0ngP@ssword" --outdir /home/user/recovered/

# رمزگشایی در پوشه مشخص (ویندوز)
python bcsae.py d document_secret.png --pass "MyStr0ngP@ssword" --outdir C:\Users\User\Desktop\
```

</div>

✅ خروجی: `document_secret.pdf` (نام و پسوند اصلی به طور خودکار بازیابی می‌شود)

---

#### مثال کامل – رمزگذاری و سپس رمزگشایی

<div dir="ltr">

```bash
# مرحله ۱: رمزگذاری
python bcsae.py e report.docx --pass "correct-horse-battery-staple"
# خروجی: report.png

# مرحله ۲: انتقال امن فایل report.png به دستگاه دیگر

# مرحله ۳: رمزگشایی
python bcsae.py d report.png --pass "correct-horse-battery-staple"
# خروجی: report.docx  (کاملاً یکسان با فایل اصلی)
```

</div>

---

### 🔐 نحوه عملکرد الگوریتم رمزگذاری

الگوریتم BCSAE مراحل زیر را به ترتیب اعمال می‌کند:

<div dir="ltr">

```
داده اصلی
    │
    ▼
① معکوس‌سازی تمام بیت‌ها (XOR با 0xFF)
    │
    ▼
② جابجایی سزار +3 (هر بایت += 3 mod 256)
    │
    ▼
③ معکوس‌سازی دوباره بیت‌ها
    │
    ▼
④ جابجایی سزار +1 (هر بایت += 1 mod 256)
    │
    ▼
⑤ XOR با keystream (از SHA-256 رمز عبور + salt تصادفی ۱۶ بایتی)
    │
    ▼
⑥ فشرده‌سازی با zlib (سطح ۹)
    │
    ▼
ذخیره نهایی درون تصویر PNG
```

</div>

**ساختار داده ذخیره‌شده درون PNG:**

<div dir="ltr">

```
[16-byte salt] [2-byte filename length] [filename bytes] [encrypted+compressed payload]
```

</div>

> Salt به صورت تصادفی تولید می‌شود، بنابراین رمزگذاری دو بار از یک فایل، دو تصویر PNG کاملاً متفاوت تولید می‌کند.

---

### ⚠️ نکات مهم

> 🔑 **امکان بازیابی رمز عبور وجود ندارد.** اگر رمز عبور خود را فراموش کنید، داده‌ها قابل بازیابی نخواهند بود. رمز عبور خود را در مکانی امن نگه دارید.

> 📦 **خروجی همیشه PNG است.** حتی اگر فایل ورودی خودش یک تصویر باشد، PNG خروجی شبیه نویز تصادفی به نظر می‌رسد.

> 💾 **تصویر PNG را دوباره فشرده یا تبدیل نکنید.** هر عملیات با افت کیفیت (تبدیل به JPEG، ویرایش با خروجی lossy) داده‌های رمزشده را برای همیشه خراب می‌کند. PNG را همیشه lossless نگه دارید.

> 🧩 **بایت‌های padding** – تبدیل به پیکسل نیاز به طول داده‌ای مضرب ۳ دارد. تعداد کمی بایت صفر (`0x00`) اضافه می‌شود که در رمزگشایی به طور خودکار حذف می‌گردد.

> ⏱ **کارایی** – فایل‌های بزرگ ممکن است زمان بیشتری بگیرند. نوار پیشرفت پیشرفت رمزگذاری/رمزگشایی را لحظه به لحظه نشان می‌دهد.

---

### 📂 ساختار پروژه

<div dir="ltr">

```
bcsae-png-encryption/
│
├── bcsae.py          # اسکریپت اصلی (رمزگذاری + رمزگشایی)
├── README.md         # این فایل
└── requirements.txt  # وابستگی‌های پایتون
```

</div>

---

### 📄 مجوز

این پروژه تحت **مجوز MIT** منتشر شده است – استفاده، تغییر و توزیع آزاد است.

</div>
