import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from config import SENDER_EMAIL, EMAIL_PASSWORD
from make_it_a_pdf import build_pdf

REPORT_PATH = "jobs_report.pdf"

RECIPIENTS = [
    "t.majstorovic@outlook.com",
    "k.christine.king21@gmail.com"
]

SUBJECT = "NEW RFP Report for ReliefWeb"

BODY = (
    "Hello Team !\n\n"
    "Find the new RFP Report for ReliefWeb attached in this email.\n"
    "CC t.majstorovic@outlook.com in your response and feel free to ask any questions you may have. \n"
    "With kind regards,\n"
    "Antonio Toni Majstorovic"
)
def send_email():

    build_pdf()

    if not os.path.exists(REPORT_PATH):
        print(f"Error: {REPORT_PATH} not found. Run make_it_a_pdf.py first.")
        return

    msg = MIMEMultipart()

    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECIPIENTS)
    msg["Subject"] = SUBJECT

    msg.attach(MIMEText(BODY, "plain"))

    with open(REPORT_PATH, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())

    encoders.encode_base64(part)

    part.add_header("Content-Disposition", f"attachment; filename={REPORT_PATH}")

    msg.attach(part)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENTS, msg.as_string())
        print(f"Email sent succesfully to: {RECIPIENTS}")
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed - check email/app password.")

    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_email()