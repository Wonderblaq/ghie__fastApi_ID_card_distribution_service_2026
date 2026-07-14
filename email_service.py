import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import base64
import os
from dotenv import load_dotenv
from pathlib import Path

# === Brevo API Config ===
# Use your API Key (the long xkeysib... one), NOT the SMTP password
# This finds the directory where your script is actually located
# Docker handles loading the .env file globally; we read directly from the environment
API_KEY = os.environ.get("API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_NAME = "GhIE Student E-Card Team"


def send_email_with_id(recipient, member_data, buffer):
    """Send the ID card via Brevo API (Bypasses Render SMTP Block)."""

    # Setup Brevo Configuration
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Prepare the PDF Attachment
    pdf_base64 = base64.b64encode(buffer).decode('utf-8')

    attachment = sib_api_v3_sdk.SendSmtpEmailAttachment(
        content=pdf_base64,
        name=f"{member_data['memberId']}.pdf"
    )


    # Create the Professional Email Body
    # Create the Professional Email Body
    body_html = f"""
            <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>GhIE Student Membership</title>
    </head>

    <body style="margin:0;padding:0;background:#f4f6f9;font-family:Arial,Helvetica,sans-serif;">

    <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6f9;padding:40px 20px;">
    <tr>
    <td align="center">

    <table width="600" cellpadding="0" cellspacing="0"
    style="
    background:#ffffff;
    border-radius:12px;
    overflow:hidden;
    box-shadow:0 4px 20px rgba(0,0,0,0.08);
    ">

        <!-- Header -->
        <tr>
            <td
            style="
            background:#0056b3;
            color:white;
            padding:35px;
            text-align:center;
            ">
                <h1 style="margin:0;font-size:28px;">
                    Ghana Institution of Engineering
                </h1>

                <p style="margin-top:10px;font-size:16px;opacity:.9;">
                    Student Membership E-Card
                </p>
            </td>
        </tr>

        <!-- Greeting -->
        <tr>
            <td style="padding:40px;">

                <h2 style="margin-top:0;color:#222;">
                    Congratulations 🎉
                </h2>

                <p style="font-size:16px;color:#555;line-height:1.7;">
                    Dear
                    <strong>{member_data['fullName']}</strong>,
                </p>

                <p style="font-size:16px;color:#555;line-height:1.7;">
                    We are pleased to inform you that your
                    <strong>GhIE Student Membership ID Card</strong>
                    has been successfully generated.
                </p>

                <p style="font-size:16px;color:#555;line-height:1.7;">
                    Your official membership card is attached to this email as a PDF.
                </p>

            </td>
        </tr>

        <!-- Member Information -->
        <tr>
            <td style="padding:0 40px 30px 40px;">

                <table
                width="100%"
                cellpadding="15"
                cellspacing="0"
                style="
                background:#f7f9fc;
                border-left:5px solid #0056b3;
                border-radius:8px;
                ">

                    <tr>
                        <td>

                            <h3 style="margin-top:0;color:#0056b3;">
                                Membership Details
                            </h3>

                            <p style="margin:8px 0;font-size:15px;">
                                <strong>Member ID:</strong><br>
                                {member_data['memberId']}
                            </p>

                            <p style="margin:8px 0;font-size:15px;">
                                <strong>Institution:</strong><br>
                                {member_data['institution']}
                            </p>

                        </td>
                    </tr>

                </table>

            </td>
        </tr>

        <!-- Instructions -->
        <tr>
            <td style="padding:0 40px;">

                <h3 style="color:#222;">
                    What's Next?
                </h3><ul style="color:#555;font-size:15px;line-height:1.8;padding-left:20px;">

                    <li>Download and save your attached membership card.</li>

                    <li>Present it whenever proof of GhIE student membership is required.</li>

                    <li>Scan the QR Code on the card to verify your membership information.</li>

                </ul>

            </td>
        </tr>

        <!-- Notice -->
        <tr>
            <td style="padding:30px 40px;">

                <table
                width="100%"
                cellpadding="18"
                cellspacing="0"
                style="
                background:#fff8e5;
                border-left:5px solid #ffb300;
                border-radius:8px;
                ">

                    <tr>
                        <td style="font-size:14px;color:#555;line-height:1.7;">

                            <strong>Important Notice</strong>

                            <br><br>

                            If you notice any incorrect information on your membership card,
                            please contact the GhIE Student E-Card Team as soon as possible for assistance.

                        </td>
                    </tr>

                </table>

            </td>
        </tr>

        <!-- Closing -->
        <tr>
            <td style="padding:0 40px 35px 40px;">

                <p style="font-size:16px;color:#555;line-height:1.7;">

                    Thank you for being a valued member of the
                    <strong>Ghana Institution of Engineering.</strong>

                </p>

                <p style="margin-top:30px;color:#555;">
                    Best Regards,
                </p>

                <p style="margin-top:5px;font-size:18px;font-weight:bold;color:#0056b3;">
                    GhIE Student E-Card Team
                </p>

            </td>
        </tr>

        <!-- Footer -->
        <tr>

            <td
            style="
            background:#f2f4f7;
            text-align:center;
            padding:25px;
            color:#777;
            font-size:13px;
            line-height:1.6;
            ">
                Please do not reply directly to this message.

                <br><br>

                ©️ 2026 Ghana Institution of Engineering (GhIE)

            </td>

        </tr>

    </table>

    </td>
    </tr>
    </table>

    </body>
    </html>
    """

    # Construct the Email Object
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": recipient, "name": member_data['fullName']}],
        sender={"name": SENDER_NAME, "email": SENDER_EMAIL},
        subject="Your GhIE Student Membership ID Card",
        html_content=body_html,
        attachment=[attachment]
    )

    try:
        # This sends via HTTP (Port 443)
        api_instance.send_transac_email(send_smtp_email)
        print(f"✅ API Sent ID card to {recipient}")
        return True
    except ApiException as e:
        print(f"❌ Brevo API Error for {recipient}: {e}")
        return False