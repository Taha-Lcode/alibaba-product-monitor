
import smtplib
from email.message import EmailMessage

EMAIL = "alibaba.notifier@gmail.com"
PASSWORD = "tmkxhwjhzohcdgzj"  # ← App Password

msg = EmailMessage()
msg["Subject"] = "Test Email"
msg["From"] = EMAIL
msg["To"] = "mohdtahasaleem@gmail.com"
msg.set_content("Test message from your Gmail bot.")

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.set_debuglevel(1)
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)
    print("✅ Email sent.")
except Exception as e:
    print("❌ Failed:", e)