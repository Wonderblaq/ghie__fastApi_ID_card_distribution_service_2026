from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from card_generator import generate_card
from card_image_to_pdf import create_pdf_from_image
from email_service import send_email_with_id

app = FastAPI()


class MemberPayload(BaseModel):
    fullName: str
    memberId: str
    institution: str
    gender: str
    region: str
    email: str
    registrationDate: str
    expiryDate: str
    photoUrl: str | None


@app.get("/home")
def root(name: str = "Wonder"):
    return {f"Hello {name} , welcome to your homepage"}


@app.post("/create_and_send_card")
def send_card(member: MemberPayload):
    image_buffer, member_data = generate_card(member.dict())
    pdf_buffer = create_pdf_from_image(image_buffer, member.memberId)
    sent = send_email_with_id(member.email, member_data, pdf_buffer)

    if sent:
        return {"status": "SUCCESS"}
    else:
        return {"status": "FAILED"}






