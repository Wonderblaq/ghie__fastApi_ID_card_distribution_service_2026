from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO

from card_image_to_pdf import create_pdf_from_image
from email_service import send_email_with_id
from card_utils import add_rounded_corners

import qrcode
import requests


# === Positions on Card ===
positions = {
    "fullName": (255, 168),
    "institution": (255, 250),
    "member_id": (255, 287),
    "start_date": (255, 329),
    "completion_date": (375, 329),
    "gender": (255, 208),
    "photo_path": (45, 146),
    "qr_code": (480, 270),
}


# === Fonts ===
font_path = "fonts/BricolageGrotesque_24pt_Condensed-Regular.ttf"
bricolage_font = ImageFont.truetype(font_path, size=21)


def generate_card(member: dict):
    """Generate the ID card image and return it as BytesIO."""

    # Open the template
    with Image.open("assets/Template.png") as base_image:

        profile = None

        try:
            # Fetch the student photo
            if member.get("photoUrl"):

                response = requests.get(
                    member["photoUrl"],
                    timeout=5
                )

                # Load downloaded image into memory
                photo_bytes = BytesIO(response.content)

                profile = Image.open(photo_bytes).convert("RGBA")

                # photo_bytes is no longer needed
                photo_bytes.close()

            else:
                profile = Image.open("assets/default_pic.jpeg")

            # Process the card
            base_resize = base_image.resize(
                (600, 384),
                Image.LANCZOS
            )

            base_resize_2 = add_rounded_corners(
                base_resize,
                20
            )

            # Prepare passport photo
            profile_cropped = ImageOps.fit(
                profile,
                (186, 209),
                Image.LANCZOS
            )

            # Create drawing object
            draw = ImageDraw.Draw(base_resize_2)

            # Prepare member data
            member_data = {
                "fullName": member.get("fullName")
                    or member.get("firstName", ""),

                "email": member.get("email", ""),

                "gender": member.get("gender", ""),

                "memberId": member.get("memberId", ""),

                "institution": member.get("institution", ""),

                "photoUrl": member.get("photoUrl", ""),

                "registrationDate": member.get(
                    "registrationDate",
                    ""
                ),

                "region": member.get("region", ""),

                "expiryDate": member.get(
                    "expiryDate",
                    ""
                ),
            }

            # === Draw text ===

            draw.text(
                positions["fullName"],
                member_data["fullName"].upper(),
                font=bricolage_font,
                fill="#2d195e"
            )

            draw.text(
                positions["completion_date"],
                str(member_data["expiryDate"]),
                font=bricolage_font,
                fill="#2d195e"
            )

            draw.text(
                positions["start_date"],
                str(member_data["registrationDate"]),
                font=bricolage_font,
                fill="#2d195e"
            )

            draw.text(
                positions["member_id"],
                str(member_data["memberId"]),
                font=bricolage_font,
                fill="#2d195e"
            )

            draw.text(
                positions["gender"],
                str(member_data["gender"]).upper(),
                font=bricolage_font,
                fill="#2d195e"
            )

            draw.text(
                positions["institution"],
                str(member_data["institution"]).upper(),
                font=bricolage_font,
                fill="#2d195e"
            )

            # === Paste profile photo ===

            base_resize_2.paste(
                profile_cropped,
                positions["photo_path"]
            )

            # === Generate QR Code ===

            qr = qrcode.QRCode(
                version=1,
                box_size=4,
                border=2
            )

            qr.add_data(
                f"https://yeghie.com/details/"
                f"{member.get('memberId', '')}"
            )

            qr.make(fit=True)

            qr_img = qr.make_image(
                fill_color="black",
                back_color="white"
            ).resize((100, 100))

            base_resize_2.paste(
                qr_img,
                positions["qr_code"]
            )


            # SAVE CARD IMAGE TO MEMORY
            # === SAVE CARD IMAGE TO MEMORY ===
            buffer = BytesIO()

            base_resize_2.save(
                buffer,
                format="PNG",
                optimize=False
            )

            # Move pointer back to the beginning so the reader starts from byte 0
            buffer.seek(0)

            # Return the OPEN buffer directly to the caller
            return buffer, member_data

        finally:
            # Only clean up resources that are safe to close
            pass


            # buffer = BytesIO()
            #
            # base_resize_2.save(
            #     buffer,
            #     format="PNG",
            #     optimize=False
            # )
            #
            # # Move pointer back to beginning
            # buffer.seek(0)
            #
            # # Return the OPEN buffer
            # return buffer, member_data

