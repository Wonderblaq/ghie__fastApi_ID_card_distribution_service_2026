from PIL import Image, ImageDraw, ImageFont, ImageOps
import smtplib
import time
from io import BytesIO
from card_image_to_pdf import create_pdf_from_image
from email_service import send_email_with_id
import qrcode
import requests


from PIL import Image, ImageDraw, ImageFont, ImageOps
from card_utils import add_rounded_corners




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
font_path = ("/Users/sarfowonder/Downloads/Bricolage_Grotesque (1)"
             "/static/BricolageGrotesque_24pt_Condensed-Regular.ttf")
bricolage_font = ImageFont.truetype(font_path, size=21)




def generate_card(member: dict):
    """Generate the ID card image and return it as BytesIO."""
    base_image = Image.open("assets/Template.png")

    # Load member photo
    try:
        if member.get("photoUrl"):
            response = requests.get(member["photoUrl"])
            profile = Image.open(BytesIO(response.content))
        else:
            profile = Image.open("assets/default_pic.jpeg")
    except Exception as e:
        print(f"⚠️ Error loading photo for {member.get('fullName')}: {e}")
        profile = Image.open("assets/default_pic.jpeg")

    base_resize = base_image.resize((600, 384), Image.LANCZOS)
    base_resize_2 = add_rounded_corners(base_resize, 20)

    passport_pic_size = (186, 209)
    profile_cropped = ImageOps.fit(profile, passport_pic_size, Image.LANCZOS)

    draw = ImageDraw.Draw(base_resize_2)

    member_data = {
        "fullName": member.get("fullName") or member.get("firstName", ""),
        "email": member.get("email", ""),
        "gender": member.get("gender", ""),
        "member_id": member.get("memberId", ""),
        "institution": member.get("institution", ""),
        "photoUrl": member.get("photoUrl", ""),
        "start_year": member.get("start_year", ""),
        "region": member.get("region", ""),
        "completion_year": member.get("completion_year", ""),

    }

    # Draw text
    draw.text(positions["fullName"], member_data["fullName"].upper(), font=bricolage_font, fill="#2d195e")
    draw.text(positions["completion_date"], str(member_data["completion_year"]), font=bricolage_font, fill="#2d195e")
    draw.text(positions["start_date"], str(member_data["start_year"]), font=bricolage_font, fill="#2d195e")
    draw.text(positions["member_id"], "GhIE-" + str(member_data["member_id"]), font=bricolage_font, fill="#2d195e")
    draw.text(positions["gender"], str(member_data["gender"]).upper(), font=bricolage_font, fill="#2d195e")
    draw.text(positions["institution"], str(member_data["institution"]).upper(), font=bricolage_font, fill="#2d195e")

    # Paste profile photo
    base_resize_2.paste(profile_cropped, positions["photo_path"])

    # Generate QR Code
    base_link = "https://yeghie.com/details/"
    full_link = base_link + str(member.get("memberId", ""))
    qr = qrcode.QRCode(version=1, box_size=4, border=2)
    qr.add_data(full_link)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((100, 100))
    base_resize_2.paste(qr_img, positions["qr_code"])

    # Save to memory
    buffer = BytesIO()
    base_resize_2.save(buffer, format="PNG")
    buffer.seek(0)



    return buffer, member_data





