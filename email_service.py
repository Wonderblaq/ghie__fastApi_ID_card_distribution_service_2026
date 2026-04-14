import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import base64
import os
from dotenv import load_dotenv
from pathlib import Path

# === Brevo API Config ===
# Use your API Key (the long xkeysib... one), NOT the SMTP password
# This finds the directory where your script is actually located
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
API_KEY = os.getenv("API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = "GhIE Student E-Card Team"


def send_email_with_id(recipient, member_data, buffer):
    """Send the ID card via Brevo API (Bypasses Render SMTP Block)."""

    # Setup Brevo Configuration
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Prepare the PDF Attachment
    buffer.seek(0)
    pdf_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    attachment = sib_api_v3_sdk.SendSmtpEmailAttachment(
        content=pdf_base64,
        name=f"{member_data['memberId']}.pdf"
    )


    # Create the Professional Email Body
    body_html = (
        f"<html>"
        f"<body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>"
        f"  <div style='max-width: 600px; margin: 20px auto; border: 1px solid #eee; padding: 20px; border-radius: 8px;'>"
        f"    <h2 style='color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;'>GhIE Student Membership</h2>"
        f"    <p>Dear <strong>{member_data['fullName']}</strong>,</p>"
        f"    <p>Congratulations! Please find your official GhIE Student Membership ID card attached to this email.</p>"
        f"    "
        f"    <div style='background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;'>"
        f"      <p style='margin: 0;'><strong>Member ID:</strong> {member_data['memberId']}</p>"
        f"      <p style='margin: 5px 0 0 0;'><strong>Institution:</strong> {member_data['institution']}</p>"
        f"    </div>"
        f"    "
        f"    <p>You can preview and verify your membership details by scanning the <strong>QR code</strong> on your card.</p>"
        f"    <p style='font-size: 0.9em; color: #666;'>If you notice any errors or discrepancies, kindly contact the GhIE Student E-Card support team immediately.</p>"
        f"    <hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0;'>"
        f"    <p style='margin-bottom: 0;'>Best regards,</p>"
        f"    <p style='margin-top: 5px;'><strong>GhIE Student E-Card Team</strong></p>"
        f"  </div>"
        f"</body>"
        f"</html>"
    )

    # Construct the Email Object
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": recipient, "name": member_data['fullName']}],
        sender={"name": SENDER_NAME, "email": SENDER_EMAIL},
        subject="Your GhIE Student Membership ID Card",
        html_content=body_html,
        attachment=[attachment]
    )

    try:
        # This sends via HTTP (Port 443) - Render allows this!
        api_instance.send_transac_email(send_smtp_email)
        print(f"✅ API Sent ID card to {recipient}")
        return True
    except ApiException as e:
        print(f"❌ Brevo API Error for {recipient}: {e}")
        return False