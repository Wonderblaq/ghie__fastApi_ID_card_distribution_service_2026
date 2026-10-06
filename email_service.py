import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import base64
import os
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# BREVO API CONFIG
# ============================================================

API_KEY = os.environ.get("API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_NAME = "GhIE Student E-Card Team"


# ============================================================
# HOSTED GHIE LOGO / BANNER
# ============================================================

LOGO_URL = (
    "https://res.cloudinary.com/dni9ie4su/image/upload/"
    "v1791296214/rj9flsw6gwynsblpijak.png"
)


def send_email_with_id(recipient, member_data, buffer):
    """Send the ID card PDF via Brevo API using the responsive HTML template."""

    # ========================================================
    # SETUP BREVO
    # ========================================================

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )


    # ========================================================
    # 1. PREPARE PDF ATTACHMENT
    # ========================================================

    pdf_base64 = base64.b64encode(buffer).decode("utf-8")

    pdf_attachment = {
        "content": pdf_base64,
        "name": f"{member_data['memberId']}.pdf"
    }


    # ========================================================
    # 2. EMAIL HTML BODY
    # ========================================================
    #
    # This is intentionally NOT an f-string.
    # That means normal CSS { } braces work without escaping.
    #
    # We insert the member information later using .replace().
    # ========================================================

    body_html = """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1">

    <meta name="color-scheme" content="light">

    <meta name="supported-color-schemes" content="light">

    <title>GhIE Student Membership</title>

    <link
        href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap"
        rel="stylesheet"
    >

    <style>

        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

        :root {
            color-scheme: light;
            supported-color-schemes: light;
        }

        body,
        table,
        td,
        p,
        h1,
        h2,
        h3,
        strong,
        span,
        a {
            font-family:
                'DM Sans',
                'Segoe UI',
                Arial,
                Helvetica,
                sans-serif;
        }

        @media only screen and (max-width: 520px) {

            .outer {
                padding: 20px 10px !important;
            }

            .px {
                padding-left: 24px !important;
                padding-right: 24px !important;
            }

            .greeting {
                font-size: 26px !important;
            }

            .member-id {
                font-size: 24px !important;
            }

        }

    </style>

</head>


<body
    style="
        margin:0;
        padding:0;
        background-color:#8AD1FF;
        font-family:'DM Sans','Segoe UI',Arial,Helvetica,sans-serif;
        -webkit-font-smoothing:antialiased;
        -webkit-text-size-adjust:100%;
    "
>


<!-- ============================================================
     INBOX PREVIEW TEXT
============================================================= -->

<div
    style="
        display:none;
        max-height:0;
        overflow:hidden;
        opacity:0;
        font-size:1px;
        line-height:1px;
        color:#8AD1FF;
    "
>
    Your GhIE Student Membership ID Card is ready and attached to this email as a PDF.
</div>


<!-- ============================================================
     OUTER BACKGROUND
============================================================= -->

<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    bgcolor="#8AD1FF"
    style="background-color:#8AD1FF;"
>

<tr>

<td
    align="center"
    class="outer"
    style="padding:40px 12px 36px;"
>


<!-- ============================================================
     MAIN EMAIL CARD
============================================================= -->

<table
    width="600"
    cellpadding="0"
    cellspacing="0"
    border="0"
    bgcolor="#ffffff"
    style="
        width:100%;
        max-width:600px;
        background-color:#ffffff;
        border-radius:24px;
        overflow:hidden;
        box-shadow:0 20px 50px rgba(5,35,89,0.22);
    "
>


<!-- ============================================================
     GHIE BANNER
============================================================= -->

<tr>

<td
    style="
        padding:0;
        line-height:0;
        font-size:0;
        background-color:#8AD1FF;
    "
>

<img
    src="__LOGO_URL__"
    alt="Ghana Institution of Engineering – Student Membership E-Card"
    width="600"
    style="
        display:block;
        width:100%;
        max-width:600px;
        height:auto;
        border:0;
        outline:none;
        text-decoration:none;
    "
>

</td>

</tr>


<!-- ============================================================
     GREETING
============================================================= -->

<tr>

<td
    class="px"
    style="padding:48px 52px 0;"
>

<p
    style="
        margin:0 0 16px;
        font-size:12px;
        font-weight:700;
        letter-spacing:2px;
        text-transform:uppercase;
        color:#052359;
    "
>

<span
    style="
        display:inline-block;
        width:28px;
        height:3px;
        background-color:#8AD1FF;
        vertical-align:middle;
        margin-right:10px;
        border-radius:2px;
    "
></span>

Membership confirmed

</p>


<h1
    class="greeting"
    style="
        margin:0 0 28px;
        font-size:34px;
        line-height:1.15;
        font-weight:700;
        letter-spacing:-0.8px;
        color:#052359;
    "
>
    Your student ID card is ready.
</h1>


<p
    style="
        margin:0 0 16px;
        font-size:16px;
        line-height:1.75;
        color:#052359;
    "
>

Dear

<strong style="font-weight:700;">
    __FULL_NAME__
</strong>,

</p>


<p
    style="
        margin:0;
        font-size:16px;
        line-height:1.75;
        color:#052359;
    "
>

Your

<strong style="font-weight:700;">
    GhIE Student Membership ID Card
</strong>

has been successfully generated.

You'll find the official card attached to this email as a PDF.

</p>

</td>

</tr>


<!-- ============================================================
     MEMBER PASS
============================================================= -->

<tr>

<td
    class="px"
    style="padding:36px 52px 0;"
>


<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    bgcolor="#052359"
    style="
        background-color:#052359;
        background-image:linear-gradient(
            135deg,
            #052359 0%,
            #0b3a8c 100%
        );
        border-radius:18px;
    "
>


<!-- Top bar -->

<tr>

<td style="padding:24px 28px 0;">

<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
>

<tr>

<td
    style="
        font-size:11.5px;
        font-weight:700;
        letter-spacing:2px;
        text-transform:uppercase;
        color:#8AD1FF;
    "
>
    GhIE &middot; Student Member
</td>


<td align="right">

<table
    cellpadding="0"
    cellspacing="0"
    border="0"
>

<tr>

<td
    bgcolor="#8AD1FF"
    style="
        background-color:#8AD1FF;
        border-radius:999px;
        padding:5px 12px;
        font-size:11px;
        font-weight:700;
        letter-spacing:0.8px;
        text-transform:uppercase;
        color:#052359;
    "
>
    Active
</td>

</tr>

</table>

</td>

</tr>

</table>

</td>

</tr>


<!-- Member ID -->

<tr>

<td style="padding:26px 28px 0;">

<p
    style="
        margin:0;
        font-size:12.5px;
        font-weight:500;
        color:#8AD1FF;
    "
>
    Member ID
</p>


<p
    class="member-id"
    style="
        margin:6px 0 0;
        font-size:30px;
        line-height:1.2;
        font-weight:700;
        letter-spacing:1.5px;
        color:#ffffff;
    "
>
    __MEMBER_ID__
</p>

</td>

</tr>


<!-- Divider -->

<tr>

<td style="padding:24px 28px 0;">

<div
    style="
        height:0;
        border-top:1px dashed #3a5fa8;
        font-size:0;
        line-height:0;
    "
>
    &nbsp;
</div>

</td>

</tr>


<!-- Institution -->

<tr>

<td style="padding:20px 28px 28px;">

<p
    style="
        margin:0;
        font-size:12.5px;
        font-weight:500;
        color:#8AD1FF;
    "
>
    Institution
</p>


<p
    style="
        margin:6px 0 0;
        font-size:16px;
        line-height:1.5;
        font-weight:600;
        color:#ffffff;
    "
>
    __INSTITUTION__
</p>

</td>

</tr>


<!-- Bottom accent -->

<tr>

<td
    height="6"
    bgcolor="#8AD1FF"
    style="
        height:6px;
        font-size:0;
        line-height:0;
        background-color:#8AD1FF;
        border-radius:0 0 18px 18px;
    "
>
    &nbsp;
</td>

</tr>


</table>

</td>

</tr>


<!-- ============================================================
     WHAT'S NEXT
============================================================= -->

<tr>

<td
    class="px"
    style="padding:48px 52px 0;"
>

<h2
    style="
        margin:0 0 6px;
        font-size:22px;
        line-height:1.3;
        font-weight:700;
        letter-spacing:-0.3px;
        color:#052359;
    "
>
    What&rsquo;s next
</h2>


<p
    style="
        margin:0 0 22px;
        font-size:14.5px;
        line-height:1.6;
        color:#052359;
        opacity:0.7;
    "
>
    Three quick things to do with your card.
</p>


<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
>


<!-- Step 1 -->

<tr>

<td
    style="
        padding:18px 0;
        border-top:1px solid #dcf0ff;
    "
>

<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
>

<tr>

<td width="56" valign="top">

<table
    cellpadding="0"
    cellspacing="0"
    border="0"
>

<tr>

<td
    align="center"
    width="38"
    height="38"
    bgcolor="#8AD1FF"
    style="
        width:38px;
        height:38px;
        background-color:#8AD1FF;
        border-radius:12px;
        font-size:15px;
        font-weight:700;
        line-height:38px;
        color:#052359;
    "
>
    1
</td>

</tr>

</table>

</td>


<td
    valign="middle"
    style="
        font-size:15px;
        line-height:1.6;
        color:#052359;
    "
>
    <strong style="font-weight:700;">
        Download and save
    </strong>
    your attached membership card.
</td>

</tr>

</table>

</td>

</tr>


<!-- Step 2 -->

<tr>

<td
    style="
        padding:18px 0;
        border-top:1px solid #dcf0ff;
    "
>

<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
>

<tr>

<td width="56" valign="top">

<table
    cellpadding="0"
    cellspacing="0"
    border="0"
>

<tr>

<td
    align="center"
    width="38"
    height="38"
    bgcolor="#8AD1FF"
    style="
        width:38px;
        height:38px;
        background-color:#8AD1FF;
        border-radius:12px;
        font-size:15px;
        font-weight:700;
        line-height:38px;
        color:#052359;
    "
>
    2
</td>

</tr>

</table>

</td>


<td
    valign="middle"
    style="
        font-size:15px;
        line-height:1.6;
        color:#052359;
    "
>
    <strong style="font-weight:700;">
        Present it
    </strong>
    whenever proof of GhIE student membership is required.
</td>

</tr>

</table>

</td>

</tr>


<!-- Step 3 -->

<tr>

<td
    style="
        padding:18px 0 0;
        border-top:1px solid #dcf0ff;
    "
>

<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
>

<tr>

<td width="56" valign="top">

<table
    cellpadding="0"
    cellspacing="0"
    border="0"
>

<tr>

<td
    align="center"
    width="38"
    height="38"
    bgcolor="#8AD1FF"
    style="
        width:38px;
        height:38px;
        background-color:#8AD1FF;
        border-radius:12px;
        font-size:15px;
        font-weight:700;
        line-height:38px;
        color:#052359;
    "
>
    3
</td>

</tr>

</table>

</td>


<td
    valign="middle"
    style="
        font-size:15px;
        line-height:1.6;
        color:#052359;
    "
>
    <strong style="font-weight:700;">
        Scan the QR code
    </strong>
    on the card to verify your membership information.
</td>

</tr>

</table>

</td>

</tr>


</table>

</td>

</tr>


<!-- ============================================================
     NOTICE
============================================================= -->

<tr>

<td
    class="px"
    style="padding:40px 52px 0;"
>


<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    bgcolor="#edf8ff"
    style="
        background-color:#edf8ff;
        border-radius:14px;
    "
>

<tr>

<td
    style="
        padding:20px 24px;
        font-size:14px;
        line-height:1.7;
        color:#052359;
    "
>

<strong
    style="
        display:block;
        margin-bottom:4px;
        font-size:12px;
        font-weight:700;
        letter-spacing:1.5px;
        text-transform:uppercase;
    "
>
    Important notice
</strong>

If you notice any incorrect information on your membership card,
please contact the GhIE Student E-Card Team as soon as possible
for assistance.

</td>

</tr>

</table>

</td>

</tr>


<!-- ============================================================
     CLOSING
============================================================= -->

<tr>

<td
    class="px"
    style="padding:40px 52px 48px;"
>

<p
    style="
        margin:0;
        font-size:15.5px;
        line-height:1.75;
        color:#052359;
    "
>
    Thank you for being a valued student member of the
    <strong style="font-weight:700;">
        Ghana Institution of Engineering.
    </strong>
</p>


<p
    style="
        margin:28px 0 0;
        font-size:15px;
        color:#052359;
    "
>
    Best regards,
</p>


<p
    style="
        margin:4px 0 0;
        font-size:18px;
        font-weight:700;
        letter-spacing:-0.2px;
        color:#052359;
    "
>
    GhIE Student E-Card Team
</p>

</td>

</tr>


<!-- ============================================================
     GRADIENT BASE
============================================================= -->

<tr>

<td
    height="8"
    bgcolor="#8AD1FF"
    style="
        height:8px;
        font-size:0;
        line-height:0;
        background-color:#8AD1FF;
        background-image:linear-gradient(
            90deg,
            #8AD1FF 0%,
            #4ea6ec 60%,
            #0b3a8c 100%
        );
    "
>
    &nbsp;
</td>

</tr>


</table>


<!-- ============================================================
     FOOTER
============================================================= -->

<table
    width="600"
    cellpadding="0"
    cellspacing="0"
    border="0"
    style="
        width:100%;
        max-width:600px;
    "
>

<tr>

<td
    align="center"
    style="
        padding:28px 20px 0;
        font-size:12.5px;
        line-height:1.9;
        color:#052359;
    "
>

<strong
    style="
        color:#052359;
        font-weight:700;
    "
>
    &copy; 2026 Ghana Institution of Engineering (GhIE)
</strong>

<br>

Need help? Call us on +233 (0)302 760 867

<br>

<span style="opacity:0.75;">
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


    # ========================================================
    # 3. INSERT DYNAMIC MEMBER DATA
    # ========================================================

    body_html = body_html.replace(
        "__LOGO_URL__",
        LOGO_URL
    )

    body_html = body_html.replace(
        "__FULL_NAME__",
        str(member_data.get("fullName", ""))
    )

    body_html = body_html.replace(
        "__MEMBER_ID__",
        str(member_data.get("memberId", ""))
    )

    body_html = body_html.replace(
        "__INSTITUTION__",
        str(member_data.get("institution", ""))
    )


    # ========================================================
    # 4. DISPATCH EMAIL VIA BREVO API
    # ========================================================

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[
            {
                "email": recipient,
                "name": member_data["fullName"]
            }
        ],

        sender={
            "name": SENDER_NAME,
            "email": SENDER_EMAIL
        },

        subject="Your GhIE Student Membership ID Card",

        html_content=body_html,

        # Only the PDF is attached.
        # The GhIE banner is loaded from Cloudinary.
        attachment=[
            pdf_attachment
        ]
    )


    # ========================================================
    # 5. SEND
    # ========================================================

    try:

        api_instance.send_transac_email(send_smtp_email)

        print(f"API Sent ID card to {recipient}")

        return True

    except ApiException as e:

        print(f"Brevo API Error for {recipient}: {e}")

        return False