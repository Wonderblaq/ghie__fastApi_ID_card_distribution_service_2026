import logging

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from io import BytesIO

# Set up clean logging to catch image issues gracefully
logger = logging.getLogger("card-service")
# # Load this once globally to save RAM
# TEMPLATE_BG = ImageReader("assets/Frame 12682.png")

# Define the asset path globally as a string constant (NOT the initialized object)
TEMPLATE_PATH = "assets/Frame 12682.png"


def create_pdf_from_image(image_bytes: bytes, member_id: str) -> bytes:
    pdf_buffer = BytesIO()

    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    page_width, page_height = A4

    # Draw Background
    c.drawImage(TEMPLATE_PATH, 0, 0, width=page_width, height=page_height, mask='auto')

    card_width, card_height = 400, 284

    # Convert bytes safely to ImageReader
    with BytesIO(image_bytes) as card_img_buffer:
        card_image = ImageReader(card_img_buffer)
        x = (page_width - card_width) / 2
        y = page_height - card_height - 220
        c.drawImage(card_image, x, y, width=card_width, height=card_height)

    c.setFont("Courier-Oblique", 15)
    c.drawString(18, 80, f"GhIE Student ID Card • Member ID: {member_id}")

    c.showPage()
    c.save()

    # Extract bytes while stream is OPEN
    pdf_data = pdf_buffer.getvalue()

    # close the buffer safely
    pdf_buffer.close()

    #Return the clean byte array
    return pdf_data