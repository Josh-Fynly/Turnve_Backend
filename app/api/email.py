from fastapi import APIRouter, HTTPException
from app.services.email_service import email_service

router = APIRouter(
    prefix="/email",
    tags=["Email"]
)


@router.get("/test")
async def test_email():
    """
    Simple test route to confirm email service responds.
    """
    return {"status": "Email API is connected."}


@router.post("/send")
async def send_custom_email(
    email: str,
    subject: str,
    message: str
):
    """
    Send a custom HTML email.
    """
    result = await email_service.send_email(
        to_email=email,
        subject=subject,
        html_content=f"<p>{message}</p>"
    )
    return result


@router.post("/otp/send")
async def send_otp(email: str, name: str):
    """
    Send OTP email (verification).
    """
    result = await email_service.send_verification_otp(email, name)
    return result


@router.post("/otp/verify")
async def verify_otp(email: str, otp: str):
    """
    Verify OTP entered by user.
    """
    result = await email_service.verify_otp(email, otp, "verification")
    return result