
# 🛍️ Alibaba Product Monitoring Agent

A Python-based intelligent monitoring agent that scrapes Alibaba for products based on your chosen keywords, stores them in a local database, and sends email alerts for **new arrivals**. Supports auto-scheduling, multiple keyword tracking, and persistent logging.

---

## 🚀 Features

- 🔍 Product scraper using Playwright
- 🧠 Tracks previously seen products
- 📨 Sends email alerts for new listings
- 🧾 Saves all results in a local SQLite database
- 📂 Remembers all searched keywords
- ⏰ Fully automated with Python scheduler
- 📜 Logs all activity to `monitor.log`

---

## 🛠 Technologies Used

| Tool / Library | Purpose |
|----------------|---------|
| Python         | Core language |
| Playwright     | Scraping dynamic content (Alibaba) |
| SQLite         | Lightweight local database |
| smtplib + EmailMessage | Sending alerts via email |
| schedule       | Task scheduling and automation |
| dotenv         | Managing secrets (email credentials) |
| logging        | Activity logs and debug support |

---

## 📁 Project Structure

```
alibaba-monitor/
├── scraper/
│   └── playwright_scraper.py       # Main scraping logic
├── db/
│   └── models.py                   # DB operations (products, keywords)
├── notifier/
│   └── email_notify.py             # Email notification system
├── main.py                         # Scheduled entry-point
├── keywords.txt (optional)         # For static keyword list
├── monitor.log                     # Logs for all activity
├── .env                            # Secure email credentials
└── README.md
```

---

## 🧩 Functional Modules

### ✅ 1. **Scraper (Playwright)**
- Dynamic scraping from Alibaba.com
- Scrolls, loads content, and extracts:
  - Title
  - Product URL
  - Supplier
  - Price
  - MOQ
  - Rating

### ✅ 2. **Database (SQLite)**
- Table `products`: stores all product details, avoids duplicates
- Table `search_history`: remembers all keywords ever searched

### ✅ 3. **Email Notifications**
- Sends detailed product info to a user’s email
- Uses Gmail App Password for secure SMTP login
- Sends alerts **only for new products**

### ✅ 4. **Keyword Tracking**
- Keywords are saved from user input
- Can be reused automatically by the monitor

### ✅ 5. **Scheduled Automation**
- Uses `schedule` library to run `main.py` every X hours
- Automatically loops through all saved keywords
- Sends emails and logs activity without manual input

### ✅ 6. **Logging**
- `monitor.log` contains:
  - Timestamps
  - Products saved
  - Emails sent
  - Errors during scraping or sending

---

## ✅ Setup Instructions

### 1. Clone this repository
```bash
git clone https://github.com/yourname/alibaba-monitor.git
cd alibaba-monitor
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
playwright install
```

### 4. Configure `.env` file
Create a `.env` file:

```env
EMAIL_ADDRESS=yourbot@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=your_personal_email@gmail.com
```

> You must enable 2FA and generate an **App Password** on Gmail.

---

## 🧪 How to Use

### 📦 Manual Use (for testing)

```bash
python scraper/playwright_scraper.py
```

- Enter a keyword (e.g., “solar panel”)
- Email is sent if new product found

### 🔁 Automated Mode

```bash
python main.py
```

- Runs once immediately
- Then runs every 6 hours (or as configured)
- Logs activity to `monitor.log`

---

## 🕒 Changing Schedule

In `main.py`, update:

```python
schedule.every(6).hours.do(run_monitor)
```

To:

- `schedule.every().day.at("09:00").do(run_monitor)`
- `schedule.every(30).minutes.do(run_monitor)`

---

## 📝 Log File Output Example

```
2025-06-03 12:00:00 - INFO - 🚀 Monitor started
2025-06-03 12:00:01 - INFO - 🆕 New product saved: Smart Solar Panel
2025-06-03 12:00:02 - INFO - Email sent for: Smart Solar Panel
2025-06-03 12:00:05 - INFO - ✅ Monitor finished
```

---

## 🧼 TODO / Improvements

- Add Telegram/WhatsApp notifications
- Web UI to manage keywords
- Multi-user support
- Browserless deployment via Playwright Cloud

---

## 👨‍💻 Author

**Mohd Taha Saleem**  
BTech CSE @ Jamia Hamdard  
Tech enthusiast, problem solver, and full-stack dev  
✨ Open to contributions, feedback, and collabs!

---
