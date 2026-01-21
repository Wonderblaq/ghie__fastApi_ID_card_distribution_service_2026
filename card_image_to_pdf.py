from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from io import BytesIO




def create_pdf_from_image(image_buffer, member_id):
    # Convert PNG card image in memory into a PDF and return the PDF buffer
    # Create PDF canvas
    pdf_buffer = BytesIO()
    # Card size on PDF
    page_width = 400
    page_width= 600
    page_width,  page_height = A4

    # page_size = (page_width, page_height)
    c = canvas.Canvas(pdf_buffer, pagesize=A4)


    # Draw Bcakground using figma designed sheet
    custom_sheet_bg = ImageReader("assets/Frame 12682.png")

    c.drawImage(
        custom_sheet_bg, 0, 0, width=page_width, height=page_height, mask='auto'
    )


    card_width = 400
    card_height = 284

    # Read image from buffer
    image_buffer.seek(0)
    card_image = ImageReader(image_buffer)



    # Position card (adjust once, then forget forever)
    x = (page_width - card_width) / 2
    y = page_height - card_height - 220

    # Draw image on PDF
    c.drawImage(card_image, x, y, width=card_width, height=card_height)

    # Add footer text
    c.setFont("Courier-Oblique", 15)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(18, 80, f"GhIE Student ID Card • Member ID: {member_id} ")


    c.save()

    pdf_buffer.seek(0)
    return pdf_buffer