import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import *


class Mailer:
    def __init__(self):
        self.session = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        self.session.starttls()
        self.session.login(SENDER_ADDR, SENDER_PASS)

    def send_mail(self, subject: str, content: str, receivers: list):
        message = MIMEMultipart()
        message['From'] = SENDER_ADDR
        message['To'] = ", ".join(receivers)
        message['Subject'] = subject
        message.attach(MIMEText(content, 'html'))
        text = message.as_string()
        self.session.sendmail(SENDER_ADDR, receivers, text)
