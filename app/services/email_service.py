"""
TURNVE Email Service (MailerSend Edition)
- HTML templating with Jinja2
- OTP generation + verification
- Welcome email / job alerts / newsletters / interview reminders
- Async HTTPX MailerSend API integration
"""

import logging
import random
import string
from typing import Any, Dict, Optional, List
from datetime import datetime, timedelta
from pathlib import Path

import httpx
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.config import settings

logger = logging.getLogger(__name__)


# ============================================================
# TEMPLATE SERVICE (Jinja2)
# ============================================================

class EmailTemplateService:
    """Loads and renders email templates from app/templates/emails."""

    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent / "templates" / "emails"
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )

        logger.info(f"[EmailTemplateService] Templates dir: {self.templates_dir}")

    def load(self, template_name: str):
        try:
            return self.jinja_env.get_template(template_name)
        except Exception as e:
            logger.error(f"Unable to load template {template_name}: {e}")
            raise

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        try:
            template = self.load(template_name)
            return template.render(**context)
        except Exception as e:
            logger.error(f"Template render error in {template_name}: {e}")
            return f"<html><body><h3>Template Error</h3><p>{str(e)}</p></body></html>"


# ============================================================
# MAILERSEND EMAIL SERVICE
# ============================================================

class EmailService:
    """MailerSend-powered email system with template support."""

    def __init__(self):
        self.api_key = settings.MAILERSEND_API_KEY
        self.sender_email = settings.MAILERSEND_SENDER_EMAIL
        self.sender_name = settings.MAILERSEND_SENDER_NAME

        self.base_url = "https://api.mailersend.com/v1/email"
        self.templates = EmailTemplateService()

        # In production → replace with Redis
        self._otp_store: Dict[str, Dict[str, Any]] = {}

        if not self.api_key:
            logger.warning("MAILERSEND_API_KEY missing! Email sending will fail.")
        else:
            logger.info("MailerSend EmailService initialized.")

    # ============================================================
    # UTILS
    # ============================================================

    def generate_otp(self, length: int = 6) -> str:
        return ''.join(random.choices(string.digits, k=length))

    # Store OTP temporarily
    async def _store_otp(self, email: str, code: str, purpose: str, minutes: int):
        key = f"{email}:{purpose}"
        expire_at = datetime.utcnow() + timedelta(minutes=minutes)

        self._otp_store[key] = {
            "code": code,
            "purpose": purpose,
            "created_at": datetime.utcnow(),
            "expires_at": expire_at
        }

    async def _get_otp(self, email: str, purpose: str):
        return self._otp_store.get(f"{email}:{purpose}")

    async def _delete_otp(self, email: str, purpose: str):
        key = f"{email}:{purpose}"
        if key in self._otp_store:
            del self._otp_store[key]

    # ============================================================
    # CORE SEND EMAIL
    # ============================================================

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        to_name: Optional[str] = None,
        text_content: Optional[str] = None
    ) -> Dict[str, Any]:

        if not self.api_key:
            return {"success": False, "error": "MailerSend API key missing"}

        payload = {
            "from": {
                "email": self.sender_email,
                "name": self.sender_name
            },
            "to": [{"email": to_email, "name": to_name or ""}],
            "subject": subject,
            "html": html_content
        }

        if text_content:
            payload["text"] = text_content

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                res = await client.post(self.base_url, json=payload, headers=headers)

                if res.status_code in (200, 202):
                    logger.info(f"Email sent to {to_email}")
                    return {"success": True, "message": "Email sent"}

                error_msg = f"MailerSend error {res.status_code}: {res.text}"
                logger.error(error_msg)

                return {"success": False, "error": error_msg}

        except Exception as e:
            logger.error(f"MailerSend request failed: {e}")
            return {"success": False, "error": str(e)}

    # ============================================================
    # TEMPLATE EMAILS
    # ============================================================

    async def send_welcome_email(self, email: str, name: str, verification_url: str = None):
        html = self.templates.render("welcome.html", {
            "name": name,
            "verification_url": verification_url,
            "platform_url": settings.platform_url,
            "year": datetime.now().year
        })

        return await self.send_email(
            email,
            subject="Welcome to TURNVE!",
            html_content=html,
            to_name=name
        )

    async def send_verification_otp(self, email: str, name: str):
        """Email verification OTP"""

        code = self.generate_otp()
        await self._store_otp(email, code, "verification", minutes=10)

        html = self.templates.render("otp_verification.html", {
            "name": name,
            "otp_code": code,
            "purpose": "Verify your email",
            "expires": "10 minutes",
            "year": datetime.now().year
        })

        result = await self.send_email(
            email,
            subject=f"Your TURNVE verification code: {code}",
            html_content=html,
            to_name=name
        )

        return {**result, "otp_code": code}

    async def send_password_reset_otp(self, email: str, name: str):
        """Password reset OTP"""

        code = self.generate_otp()
        await self._store_otp(email, code, "reset", minutes=10)

        html = self.templates.render("otp_verification.html", {
            "name": name,
            "otp_code": code,
            "purpose": "Reset your password",
            "expires": "10 minutes",
            "year": datetime.now().year
        })

        result = await self.send_email(
            email,
            subject=f"Your TURNVE reset code: {code}",
            html_content=html,
            to_name=name
        )

        return {**result, "otp_code": code}

    async def send_login_otp(self, email: str, name: str):
        """Login OTP"""

        code = self.generate_otp()
        await self._store_otp(email, code, "login", minutes=5)

        html = self.templates.render("otp_verification.html", {
            "name": name,
            "otp_code": code,
            "purpose": "Login verification",
            "expires": "5 minutes",
            "year": datetime.now().year
        })

        result = await self.send_email(
            email,
            subject=f"Your TURNVE login code: {code}",
            html_content=html,
            to_name=name
        )

        return {**result, "otp_code": code}

    # ============================================================
    # VERIFY OTP
    # ============================================================

    async def verify_otp(self, email: str, code: str, purpose: str):
        stored = await self._get_otp(email, purpose)

        if not stored:
            return {"success": False, "error": "OTP expired or not found"}

        if stored["code"] != code:
            return {"success": False, "error": "Invalid OTP"}

        if datetime.utcnow() > stored["expires_at"]:
            await self._delete_otp(email, purpose)
            return {"success": False, "error": "OTP expired"}

        await self._delete_otp(email, purpose)
        return {"success": True, "message": "OTP verified"}

    # ============================================================
    # OTHER EMAIL TYPES
    # ============================================================

    async def send_cv_ready(self, email: str, name: str, download_url: str):
        html = self.templates.render("cv_ready.html", {
            "name": name,
            "cv_download_url": download_url,
            "year": datetime.now().year
        })

        return await self.send_email(
            email,
            subject="Your TURNVE CV is ready!",
            html_content=html,
            to_name=name
        )

    async def send_interview_reminder(self, email: str, name: str, details: Dict[str, Any]):
        html = self.templates.render("interview_reminder.html", {
            "name": name,
            **details,
            "year": datetime.now().year
        })

        return await self.send_email(
            email,
            subject=f"Interview Reminder — {details.get('position')}",
            html_content=html,
            to_name=name
        )

    async def send_job_alert(self, email: str, name: str, jobs: List[Dict[str, Any]]):
        html = self.templates.render("job_alert.html", {
            "name": name,
            "jobs": jobs,
            "count": len(jobs),
            "year": datetime.now().year
        })

        return await self.send_email(
            email,
            subject=f"{len(jobs)} New Job Opportunities for You",
            html_content=html,
            to_name=name
        )

    async def send_newsletter(self, email: str, name: str, newsletter: Dict[str, Any]):
        html = self.templates.render("newsletter.html", {
            "name": name,
            **newsletter,
            "year": datetime.now().year
        })

        return await self.send_email(
            email,
            subject=newspaper.get("title", "TURNVE Newsletter"),
            html_content=html,
            to_name=name
        )


# SINGLETON INSTANCE
email_service = EmailService()