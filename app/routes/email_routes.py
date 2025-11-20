from fastapi import APIRouter, HTTPException
from app.services.email_service import email_service
from pydantic import BaseModel, EmailStr

router = APIRouter(
    prefix="/email",
    tags=["Email"]
)

class SendEmailRequest(BaseModel):
    email: EmailStr
    name: str

@router.post("/send-welcome")
async def send_welcome_email(payload: SendEmailRequest):
    result = await email_service.send_welcome_email(
        email=payload.email,
        name=payload.name
    )
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@router.post("/send-verification-otp")
async def send_verification_otp(payload: SendEmailRequest):
    result = await email_service.send_verification_otp(
        email=payload.email,
        name=payload.name
    )
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@router.post("/send-password-reset-otp")
async def send_password_reset_otp(payload: SendEmailRequest):
    result = await email_service.send_password_reset_otp(
        email=payload.email,
        name=payload.name
    )
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    return result