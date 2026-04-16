from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi import Request
from card_generator import generate_card
from card_image_to_pdf import create_pdf_from_image
from email_service import send_email_with_id
from typing import Optional, List

app = FastAPI()


class MemberPayload(BaseModel):
    fullName: str
    memberId: str
    institution: str
    gender: str
    region: Optional[str] = None
    program: Optional[str] = None
    email: str
    registrationDate: str
    expiryDate: str
    photoUrl: str | None


@app.get("/home")
def root(name: str = "Wonder"):
    return {f"Hello {name} , welcome to your homepage"}


# Receives Single Object from java backend, process and then send card to email
@app.post("/create_and_send_card")
def send_card(members: MemberPayload):
    # Process member data on ID card and PDF
    image_buffer, member_data = generate_card(members.dict())
    pdf_buffer = create_pdf_from_image(image_buffer, members.memberId)

    # Send processed data to member's email and display info
    sent = send_email_with_id(members.email, member_data, pdf_buffer)
    return {"success" if sent else "failure": sent}


# This endpoint allows sending cards in batches
@app.post("/send_batch_cards")
def send_batch_card(members: List[MemberPayload]): # Added List to handle batch request
    results = []
    for member in members:
        # Process member data on ID card and PDF
        image_buffer, member_data = generate_card(member.dict())
        pdf_buffer = create_pdf_from_image(image_buffer, member.memberId)

        # Send processed data to member's email and display info
        sent = send_email_with_id(member.email, member_data, pdf_buffer)
        results.append({"email": member.email,
                        "status": "success" if sent else "failed"})
    return dict(processed_card=len(results), details=results)








