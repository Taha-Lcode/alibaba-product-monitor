import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from notifier.email_notify import send_email

send_email(
    subject="🚀 Test Email",
    body="This is a test from your Alibaba bot",
    to_address="mohdtahasaleem@gmail.com"
)
