import logging
import random
import string
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.config import settings

logger = logging.getLogger(__name__)


# ============================================================
# TEMPLATE SERVICE (JINJA2)
# ============================================================

class EmailTemplateService:
    """Loads and renders email templates stored in app/templates/emails."""

    def __init__(self):
        self.templates_dir = (
            Path(__file__).parent.parent / "templates" / "emails"
        )

        # Create directory if missing
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )

        logger.info(f"EmailTemplateService using directory: {self.templates_dir}")

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            logger.error(f"Template error ({template_name}): {e}")
            return f"""
            <html><body>
                <h3>Template Error</h3>
                <p>{str(e)}</p>
            </body></html>
            """


# ============================================================
# MAILERSEND EMAIL SERVICE
# ============================================================

class EmailService:
    """MailerSend-powered transactional email service."""

    def __init__(self):
        self.api_key = settings.mailersend_api_key
        self.sender_email = settings.mailersend_sender_email
        self.sender_name = settings.mailersend_sender_name
        self.api_url = "https://api.mailersend.com/v1/email"

        self.templates = EmailTemplateService()
        self._otp_store = {}

        if not self.api_key:
            logger.warning("MAILERSEND_API_KEY missing — email service disabled.")
        else:
            logger.info("MailerSend EmailService initialized.")

    # ------------------------------------------------------------
    # OTP GENERATOR
    # ------------------------------------------------------------
    def generate_otp(self, length: int = 6) -> str:
        return ''.join(random.choices(string.digits, k=length))

    # ------------------------------------------------------------
    # CORE SEND FUNCTION (MailerSend)
    # ------------------------------------------------------------
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        to_name: Optional[str] = None
    ) -> Dict[str, Any]:

        if not self.api_key:
            return {"success": False, "error": "MailerSend API key not set"}

        payload = {
            "from": {
                "email": self.sender_email,
                "name": self.sender_name
            },
            "to": [
                {
                    "email": to_email,
                    "name": to_name or ""
                }
            ],
            "subject": subject,
            "html": html_content
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(self.api_url, headers=headers, json=payload)

                if response.status_code in (200, 202):
                    data = response.json()
                    logger.info(f"Email sent → {to_email}")
                    return {"success": True, "id": data.get("message_id")}

                logger.error(f"MailerSend Error: {response.status_code} {response.text}")
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }

        except Exception as e:
            logger.error(f"MailerSend Exception: {e}")
            return {"success": False, "error": str(e)}

    # ============================================================
    # EMAIL TYPES
    # ============================================================

    async def send_welcome_email(self, email: str, name: str):
        context = {
            "name": name,
            "platform_url": settings.platform_url,
            "current_year": datetime.now().year
        }
        html = self.templates.render("welcome.html", context)

        return await self.send_email(
            to_email=email,
            subject="Welcome to TurnVe 🎉",
            html_content=html,
            to_name=name
        )

    async def send_verification_otp(self, email: str, name: str):
        otp = self.generate_otp()
        self.store_otp(email, otp, "verify", 10)

        context = {
            "name": name,
            "otp_code": otp,
            "expires_in": "10 minutes",
            "current_year": datetime.now().year
        }

        html = self.templates.render("otp_verification.html", context)

        result = await self.send_email(
            to_email=email,
            subject=f"Your TurnVe Verification Code: {otp}",
            html_content=html,
            to_name=name
        )

        return {**result, "otp": otp}

    async def send_password_reset_otp(self, email: str, name: str):
        otp = self.generate_otp()
        self.store_otp(email, otp, "password_reset", 10)

        context = {
            "name": name,
            "otp_code": otp,
            "expires_in": "10 minutes",
            "current_year": datetime.now().year
        }

        html = self.templates.render("otp_verification.html", context)

        result = await self.send_email(
            to_email=email,
            subject=f"Your TurnVe Password Reset Code: {otp}",
            html_content=html,
            to_name=name
        )

        return {**result, "otp": otp}

    async def send_login_otp(self, email: str, name: str):
        otp = self.generate_otp()
        self.store_otp(email, otp, "login", 5)

        context = {
            "name": name,
            "otp_code": otp,
            "expires_in": "5 minutes",
            "current_year": datetime.now().year
        }

        html = self.templates.render("otp_verification.html", context)

        result = await self.send_email(
            to_email=email,
            subject=f"Your TurnVe Login Code: {otp}",
            html_content=html,
            to_name=name
        )

        return {**result, "otp": otp}

    async def send_cv_ready_notification(self, email: str, name: str, cv_url: str):
        context = {
            "name": name,
            "cv_download_url": cv_url,
            "current_year": datetime.now().year
        }

        html = self.templates.render("cv_ready.html", context)

        return await self.send_email(
            to_email=email,
            subject="Your CV is Ready 📄",
            html_content=html,
            to_name=name
        )

    async def send_interview_reminder(self, email: str, name: str, details: Dict[str, Any]):
        context = {
            **details,
            "name": name,
            "current_year": datetime.now().year
        }

        html = self.templates.render("interview_reminder.html", context)

        return await self.send_email(
            to_email=email,
            subject=f"Interview Reminder: {details.get('position')}",
            html_content=html,
            to_name=name
        )

    async def send_job_alert(self, email: str, name: str, jobs: List[Dict[str, Any]]):
        context = {
            "name": name,
            "jobs": jobs,
            "job_count": len(jobs),
            "current_year": datetime.now().year
        }

        html = self.templates.render("job_alert.html", context)

        return await self.send_email(
            to_email=email,
            subject=f"{len(jobs)} New Job Matches 🔎",
            html_content=html,
            to_name=name
        )

    async def send_newsletter(self, email: str, name: str, content: Dict[str, Any]):
        context = {
            "name": name,
            "newsletter": content,
            "current_year": datetime.now().year
        }

        html = self.templates.render("newsletter.html", context)

        return await self.send_email(
            to_email=email,
            subject=content.get("title", "TurnVe Newsletter"),
            html_content=html,
            to_name=name
        )

    # ============================================================
    # OTP STORAGE (Replace with Redis later)
    # ============================================================

    def store_otp(self, email: str, otp: str, purpose: str, minutes: int):
        key = f"{email}:{purpose}"
        self._otp_store[key] = {
            "otp": otp,
            "expires_at": datetime.utcnow() + timedelta(minutes=minutes)
        }

    def verify_otp(self, email: str, otp: str, purpose: str) -> bool:
        key = f"{email}:{purpose}"
        data = self._otp_store.get(key)

        if not data:
            return False
        if datetime.utcnow() > data["expires_at"]:
            del self._otp_store[key]
            return False

        if otp != data["otp"]:
            return False

        del self._otp_store[key]
        return True


# Export instance
email_service = EmailService()