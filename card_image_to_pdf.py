import logging
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from io import BytesIO

logger = logging.getLogger("card-service")
TEMPLATE_PATH = "assets/template_background.png"


def create_pdf_from_image(image_bytes: bytes, member_id: str) -> bytes:
    pdf_buffer = BytesIO()

    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    page_width, page_height = A4

    # Draw Background
    c.drawImage(TEMPLATE_PATH, 0, 0, width=page_width, height=page_height, mask='auto')

    # MANUAL DIMENSIONS & POSITIONING (Tweak these values)
    card_width = 500  # Target width in ReportLab points
    card_height = 320  # Target height (maintains 1.5625 aspect ratio)

    # Calculate horizontal center
    x = (page_width - card_width) / 2  # 47.635 pt

    # Vertical offset from bottom of page
    y = 310

    # Draw Card Image with PNG Alpha Mask
    with BytesIO(image_bytes) as card_img_buffer:
        card_image = ImageReader(card_img_buffer)
        c.drawImage(card_image, x, y, width=card_width, height=card_height, mask='auto')

    # 3. Footer Text
    # c.setFont("Courier-Oblique", 13)
    # c.drawString(48, 80, f"GhIE Student ID Card • Member ID: {member_id}")

    c.showPage()
    c.save()

    pdf_data = pdf_buffer.getvalue()
   # print(f"PDF size: {len(pdf_data) / (1024 * 1024):.2f} MB")
    pdf_buffer.close()

    return pdf_data