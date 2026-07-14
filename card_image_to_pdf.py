import logging
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

# Set up clean logging to catch image issues gracefully
logger = logging.getLogger("card-service")

# Define the asset path globally as a string constant (NOT the initialized object)
TEMPLATE_PATH = "assets/Frame 12682.png"

def create_pdf_from_image(image_bytes: bytes, member_id: str) -> bytes:
    """
    Generates a secure, uncorrupted PDF by keeping stream buffers open
    until the canvas writes completely to the master buffer.
    """
    # 1. Initialize the master PDF buffer
    pdf_buffer = BytesIO()

    try:
        # 2. Instantiate the canvas directly writing to the master buffer
        c = canvas.Canvas(pdf_buffer, pagesize=A4)
        page_width, page_height = A4

        # 3. Load the background image FRESH per-request for thread safety
        try:
            background_img = ImageReader(TEMPLATE_PATH)
            c.drawImage(background_img, 0, 0, width=page_width, height=page_height, mask='auto')
        except Exception as bg_err:
            logger.error(f"Failed loading template background '{TEMPLATE_PATH}': {bg_err}")
            raise bg_err

        # 4. Keep the image bytes buffer open during the entire canvas session!
        # Do NOT close this buffer until c.save() has finished writing to pdf_buffer.
        card_img_buffer = BytesIO(image_bytes)
        card_image = ImageReader(card_img_buffer)

        # Set card layout dimensions
        card_width, card_height = 400, 284
        x = (page_width - card_width) / 2
        y = page_height - card_height - 220

        # Register the draw intent
        c.drawImage(card_image, x, y, width=card_width, height=card_height)

        # 5. Draw text overlays
        c.setFont("Courier-Oblique", 15)
        c.drawString(18, 80, f"GhIE Student ID Card • Member ID: {member_id}")

        # 6. Finalize canvas and write output to the master buffer
        c.showPage()
        c.save()  # <--- ReportLab reads card_img_buffer and TEMPLATE_PATH here!

        # 7. Safely close your child buffers now that the compilation is complete
        card_img_buffer.close()

        # 8. Return the generated PDF bytes
        return pdf_buffer.getvalue()

    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR during PDF generation: {e}", exc_info=True)
        raise e

    finally:
        # Always clean up the main PDF memory buffer
        pdf_buffer.close()

# import logging
#
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.utils import ImageReader
# from reportlab.pdfgen import canvas
# from io import BytesIO
#
# # Set up clean logging to catch image issues gracefully
# logger = logging.getLogger("card-service")
# # # Load this once globally to save RAM
# # TEMPLATE_BG = ImageReader("assets/Frame 12682.png")
#
# # Define the asset path globally as a string constant (NOT the initialized object)
# TEMPLATE_PATH = "assets/Frame 12682.png"
#
#
# def create_pdf_from_image(image_bytes : bytes, member_id : str):
#     with BytesIO() as pdf_buffer:
#         c = canvas.Canvas(pdf_buffer, pagesize=A4)
#         page_width, page_height = A4
#
#         # Draw Background (Using the global asset)
#         c.drawImage(TEMPLATE_PATH, 0, 0, width=page_width, height=page_height, mask='auto')
#
#         card_width, card_height = 400, 284
#
#         # Convert bytes safely back to ImageReader
#         with BytesIO(image_bytes) as card_img_buffer:
#             card_image = ImageReader(card_img_buffer)
#             x = (page_width - card_width) / 2
#             y = page_height - card_height - 220
#             c.drawImage(card_image, x, y, width=card_width, height=card_height)
#
#         c.setFont("Courier-Oblique", 15)
#         c.drawString(18, 80, f"GhIE Student ID Card • Member ID: {member_id}")
#
#
#         c.showPage()  # Explicitly finalize the structural layout canvas page boundary
#         c.save()  # Write all pending asset tokens completely out to the stream buffer
#
#         pdf_buffer.close()  # Push any floating metadata bytes down into the array
#
#         return pdf_buffer.getvalue()