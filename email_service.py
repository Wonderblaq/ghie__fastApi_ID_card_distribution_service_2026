from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


# === Email Config ===
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
SENDER = "Admin@yeghie.com"
SMTP_USERNAME = "969923002@smtp-brevo.com"
SMTP_PASSWORD = "3K4AnPmTw8fBHjqY"


def send_email_with_id(recipient, member_data, buffer):
    """Send the ID card via email."""
    subject = "Your GhiE Student Membership ID Card"
    body = (
        f"Dear {member_data['fullName']},\n\n"
        "Please find attached your official GhIE Student Membership ID card.\n\n"
        f"Member ID: {member_data['member_id']}\n"
        f"Institution: {member_data['institution']}\n\n"
        "You can preview and verify your membership details by scanning the QR code on your card.\n"
        "If you notice any errors or discrepancies, kindly contact the GhIE Student E-Card support team "
        "immediately.\n\n"
        "Best regards,\n"
        "GhIE Student E-Card Team"
    )

    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach the card image
    # part = MIMEBase("application", "octet-stream")
    # part.set_payload(buffer.read())
    # encoders.encode_base64(part)
    # part.add_header("Content-Disposition", f"attachment; filename={member_data['member_id']}.png")
    # msg.attach(part)

    # === NEW PDF ATTACHMENT ===
    pdf_part = MIMEBase("application", "pdf")
    buffer.seek(0)
    pdf_part.set_payload(buffer.read())
    encoders.encode_base64(pdf_part)
    pdf_part.add_header("Content-Disposition", f"attachment; filename=GHIE-{member_data['member_id']}.pdf")
    msg.attach(pdf_part)
    # ==========================

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"✅ Sent ID card to {recipient}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email to {recipient}: {e}")
        return False

