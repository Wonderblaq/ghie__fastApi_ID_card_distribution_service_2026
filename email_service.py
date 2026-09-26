import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import base64
import io
import os
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# === Brevo API Config ===
API_KEY = os.environ.get("API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_NAME = "GhIE Student E-Card Team"

LOGO_PATH = Path(__file__).resolve().parent / "assets" / "ghie_logo.jpg"

# Max width/height (px) for the logo file that gets attached to the email.
# Brevo can't render it inline in the header (see note below), so it shows
# as a normal attachment next to the PDF - a smaller file keeps that
# thumbnail small instead of a large image.....
LOGO_MAX_DIMENSION = 300


def _prepare_logo_base64(path: Path, max_dimension: int) -> str:
    """Resize the logo down to max_dimension x max_dimension (keeping aspect
    ratio) and return it as base64. Keeps the attachment thumbnail small."""
    with Image.open(path) as img:
        img = img.convert("RGB")
        img.thumbnail((max_dimension, max_dimension), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85, optimize=True)
        return base64.b64encode(buf.getvalue()).decode("utf-8")


def send_email_with_id(recipient, member_data, buffer):
    """Send the ID card via Brevo API."""

    # Setup Brevo Configuration
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    # 1. Prepare PDF Attachment as Dictionary
    pdf_base64 = base64.b64encode(buffer).decode('utf-8')
    pdf_attachment = {
        "content": pdf_base64,
        "name": f"{member_data['memberId']}.pdf"
    }

    # 2. Prepare the GhIE logo as a normal attachment (Brevo's API does not
    # support real inline/cid images - confirmed by Brevo support - so it
    # will always show as its own attachment next to the PDF, not inside the
    # email header). Resized down so that attachment stays small.
    try:
        logo_base64 = _prepare_logo_base64(LOGO_PATH, LOGO_MAX_DIMENSION)
    except FileNotFoundError:
        print(f"GhIE logo not found at: {LOGO_PATH}")
        return False

    logo_attachment = {
        "content": logo_base64,
        "name": "ghie_logo.jpg"
    }

    # 3. Email HTML Body (no logo in the header - see note above)
    body_html = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="color-scheme" content="light">
    <meta name="supported-color-schemes" content="light">

    <title>GhIE Student Membership</title>

    <style>
        :root {{
            color-scheme: light;
            supported-color-schemes: light;
        }}

        @media only screen and (max-width: 520px) {{
            .outer {{
                padding: 20px 8px !important;
            }}

            .px {{
                padding-left: 22px !important;
                padding-right: 22px !important;
            }}

            .h1 {{
                font-size: 22px !important;
            }}
        }}
    </style>

</head>


<body style="
    margin:0;
    padding:0;
    font-family:'Inter','Segoe UI',Arial,Helvetica,sans-serif;
    -webkit-font-smoothing:antialiased;
    -webkit-text-size-adjust:100%;
">


<!-- Inbox preview text -->

<div style="
    display:none;
    max-height:0;
    overflow:hidden;
    opacity:0;
    font-size:1px;
    line-height:1px;
    color:#ffffff;
">
    Your GhIE Student Membership ID Card is ready and attached to this email as a PDF.
</div>


<table width="100%" cellpadding="0" cellspacing="0">

<tr>

<td align="center"
    class="outer"
    style="padding:32px 12px;">


<table width="600"
       cellpadding="0"
       cellspacing="0"
       bgcolor="#ffffff"

       style="
           width:100%;
           max-width:600px;
           background-color:#ffffff;
           border-radius:20px;
           overflow:hidden;
           border:1px solid #c3d5e8;
           box-shadow:0 12px 32px #dbe5f0;
       ">


<!-- =========================================================
     HEADER (no logo - see note in Python code above)
========================================================= -->

<tr>

<td align="center"
    bgcolor="#0B4F8C"

    style="
        background-color:#0B4F8C;
        padding:20px 22px;
        color:#ffffff;
    ">


<table width="100%"
       cellpadding="0"
       cellspacing="0"
       bgcolor="#1c68ad"

       style="
           background-color:#1c68ad;
           border:1px solid #5f96cc;
           border-radius:16px;
           box-shadow:inset 0 1px 0 #8fb8de,0 8px 20px #08396a;
       ">

<tr>

<td align="center"
    style="padding:30px 20px 28px;">


<h1 class="h1"

    style="
        margin:0;
        font-family:'Poppins','Segoe UI',Arial,sans-serif;
        font-size:26px;
        line-height:1.25;
        font-weight:700;
        letter-spacing:0.2px;
        color:#ffffff;
    ">

    Ghana Institution of Engineering

</h1>


<p style="
    margin:10px 0 0;
    font-size:15px;
    color:#e3eef9;
    letter-spacing:0.3px;
">

    Student Membership E-Card

</p>


<!-- Status pill -->

<p style="
    display:inline-block;
    margin:18px 0 0;
    padding:6px 16px;
    font-size:12.5px;
    font-weight:600;
    letter-spacing:0.3px;
    color:#17603a;
    background-color:#e3f6ea;
    border:1px solid #9fd8b4;
    border-radius:999px;
    box-shadow:inset 0 1px 0 #ffffff;
">

    Your ID card is ready

</p>


</td>

</tr>

</table>

</td>

</tr>


<!-- =========================================================
     GREETING
========================================================= -->

<tr>

<td class="px"
    bgcolor="#ffffff"

    style="
        padding:40px 44px 26px;
        background-color:#ffffff;
    ">


<h2 style="
    margin:0 0 18px;
    font-family:'Poppins','Segoe UI',Arial,sans-serif;
    font-size:24px;
    line-height:1.3;
    color:#0a1f38;
">

    Congratulations 🎉

</h2>


<p style="
    margin:0 0 14px;
    font-size:16px;
    color:#0a1f38;
    line-height:1.7;
">

    Dear
    <strong style="font-weight:600;">
        {member_data['fullName']}
    </strong>,

</p>


<p style="
    margin:0 0 14px;
    font-size:15px;
    color:#334155;
    line-height:1.8;
">

    We are pleased to inform you that your
    <strong style="color:#0B4F8C;">
        GhIE Student Membership ID Card
    </strong>
    has been successfully generated.

</p>


<p style="
    margin:0;
    font-size:15px;
    color:#334155;
    line-height:1.8;
">

    Your official membership card is attached to this email as a PDF.

</p>


</td>

</tr>


<!-- =========================================================
     MEMBER INFORMATION
========================================================= -->

<tr>

<td class="px"
    bgcolor="#ffffff"

    style="
        padding:0 44px 30px;
        background-color:#ffffff;
    ">


<table width="100%"
       cellpadding="0"
       cellspacing="0"
       bgcolor="#eaf2fb"

       style="
           background-color:#eaf2fb;
           border:1px solid #bcd3ea;
           border-left:5px solid #0B4F8C;
           border-radius:12px;
           box-shadow:
               inset 0 1px 0 #ffffff,
               0 6px 16px #e3edf7;
       ">


<tr>

<td style="padding:20px 24px;">


<h3 style="
    margin:0 0 14px;
    font-family:'Poppins','Segoe UI',Arial,sans-serif;
    font-size:16px;
    color:#0B4F8C;
">

    Membership Details

</h3>


<p style="
    margin:0;
    font-size:12.5px;
    color:#5b6b80;
">

    Member ID

</p>


<p style="
    margin:2px 0 0;
    font-size:16px;
    font-weight:600;
    letter-spacing:0.3px;
    color:#0a1f38;
">

    {member_data['memberId']}

</p>


<div style="
    margin-top:14px;
    padding-top:14px;
    border-top:1px solid #bcd3ea;
">


<p style="
    margin:0;
    font-size:12.5px;
    color:#5b6b80;
">

    Institution

</p>


<p style="
    margin:2px 0 0;
    font-size:16px;
    font-weight:600;
    line-height:1.5;
    color:#0a1f38;
">

    {member_data['institution']}

</p>


</div>


</td>

</tr>

</table>

</td>

</tr>


<!-- =========================================================
     INSTRUCTIONS
========================================================= -->

<tr>

<td class="px"
    bgcolor="#ffffff"

    style="
        padding:0 44px;
        background-color:#ffffff;
    ">


<h3 style="
    margin:0 0 4px;
    font-family:'Poppins','Segoe UI',Arial,sans-serif;
    font-size:19px;
    line-height:1.35;
    color:#0B4F8C;
">

    What's Next?

</h3>


<p style="
    margin:0;
    font-size:13.5px;
    color:#5b6b80;
">

    Three things to do with your card.

</p>


<ul style="
    margin:14px 0 0;
    padding:16px 20px 16px 38px;
    line-height:1.7;
    font-size:14.5px;
    color:#0B4F8C;
    background-color:#eaf2fb;
    border:1px solid #bcd3ea;
    border-radius:12px;
    box-shadow:inset 0 1px 0 #ffffff;
">


<li style="padding:5px 0;">
    <span style="color:#334155;">
        <strong style="color:#0a1f38;">
            Download and save
        </strong>
        your attached membership card.
    </span>
</li>


<li style="padding:5px 0;">
    <span style="color:#334155;">
        <strong style="color:#0a1f38;">
            Present it
        </strong>
        whenever proof of GhIE student membership is required.
    </span>
</li>


<li style="padding:5px 0;">
    <span style="color:#334155;">
        <strong style="color:#0a1f38;">
            Scan the QR Code
        </strong>
        on the card to verify your membership information.
    </span>
</li>


</ul>

</td>

</tr>


<!-- =========================================================
     NOTICE
========================================================= -->

<tr>

<td class="px"
    bgcolor="#ffffff"

    style="
        padding:30px 44px;
        background-color:#ffffff;
    ">


<table width="100%"
       cellpadding="0"
       cellspacing="0"
       bgcolor="#fff6dc"

       style="
           background-color:#fff6dc;
           border:1px solid #efd07a;
           border-left:5px solid #F2A900;
           border-radius:12px;
           box-shadow:
               inset 0 1px 0 #ffffff,
               0 6px 16px #f5e7bd;
       ">


<tr>

<td style="
    padding:20px 24px;
    font-size:14px;
    color:#4a4a4a;
    line-height:1.7;
">


<strong style="
    font-family:'Poppins','Segoe UI',Arial,sans-serif;
    font-size:15px;
    color:#6b4300;
">

    Important Notice

</strong>


<br><br>


If you notice any incorrect information on your membership card,
please contact the GhIE Student E-Card Team as soon as possible for assistance.


</td>

</tr>

</table>

</td>

</tr>


<!-- =========================================================
     CLOSING
========================================================= -->

<tr>

<td class="px"
    bgcolor="#ffffff"

    style="
        padding:0 44px 36px;
        background-color:#ffffff;
    ">


<p style="
    margin:0;
    font-size:15px;
    color:#334155;
    line-height:1.8;
">

    Thank you for being a valued student member of the
    <strong style="color:#0B4F8C;">
        Ghana Institution of Engineering.
    </strong>

</p>


<p style="
    margin:28px 0 0;
    font-size:15px;
    color:#334155;
    border-top:1px solid #d4e0ee;
    padding-top:22px;
">

    Best Regards,

</p>


<p style="
    margin:6px 0 0;
    font-family:'Poppins','Segoe UI',Arial,sans-serif;
    font-size:18px;
    font-weight:700;
    color:#0B4F8C;
">

    GhIE Student E-Card Team

</p>


<p style="
    margin:2px 0 0;
    font-size:13px;
    color:#5b6b80;
">

    Ghana Institution of Engineering

</p>


</td>

</tr>


<!-- =========================================================
     FOOTER
========================================================= -->

<tr>

<td align="center"
    bgcolor="#08264a"

    style="
        background-color:#08264a;
        padding:28px 26px 26px;
        color:#b4c8df;
        font-size:12.5px;
        line-height:1.9;
        border-top:1px solid #1d4573;
    ">


<strong style="color:#ffffff;font-weight:600;">

    © 2026 Ghana Institution of Engineering (GhIE)

</strong>


<br>


Need help? Call us on +233 (0)302 760 867


<br>


<span style="
    display:inline-block;
    margin-top:12px;
    padding-top:12px;
    border-top:1px solid #1d4573;
    color:#8ea9c8;
">

    Please do not reply directly to this message.

</span>


</td>

</tr>


</table>

</td>

</tr>

</table>

</body>

</html>
"""

    # ============================================================
    # SEND EMAIL
    # 4. Dispatch Email with both attachments
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[
            {
                "email": recipient,
                "name": member_data['fullName']
            }
        ],
        sender={
            "name": SENDER_NAME,
            "email": SENDER_EMAIL
        },
        subject="Your GhIE Student Membership ID Card",
        html_content=body_html,
        attachment=[pdf_attachment, logo_attachment]
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        print(f"API Sent ID card to {recipient}")
        return True

    except ApiException as e:
        print(f"Brevo API Error for {recipient}: {e}")
        return False