# app/services/paystack_service.py
import json
import hmac
import hashlib
from typing import Optional, Dict, Any
import httpx
from app.core.config import settings
import logging

logger = logging.getLogger("paystack_service")
BASE_URL = getattr(settings, "paystack_base_url", "https://api.paystack.co")


def _headers() -> Dict[str, str]:
    key = getattr(settings, "paystack_secret_key", None)
    if not key:
        import os
        key = os.getenv("PAYSTACK_SECRET_KEY")
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


class PaystackService:
    """Encapsulate Paystack interactions."""

    @staticmethod
    async def initialize_transaction(email: str, amount_kobo: int, metadata: Optional[dict] = None, callback_url: Optional[str] = None) -> dict:
        payload = {
            "email": email,
            "amount": int(amount_kobo),
            "metadata": metadata or {},
        }
        if callback_url:
            payload["callback_url"] = callback_url

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(f"{BASE_URL}/transaction/initialize", json=payload, headers=_headers())
            resp.raise_for_status()
            return resp.json()

    @staticmethod
    async def verify_transaction(reference: str) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(f"{BASE_URL}/transaction/verify/{reference}", headers=_headers())
            resp.raise_for_status()
            return resp.json()

    @staticmethod
    def verify_webhook_signature(body: bytes, signature: str) -> bool:
        secret = getattr(settings, "paystack_webhook_secret", None)
        if not secret:
            import os
            secret = os.getenv("PAYSTACK_WEBHOOK_SECRET")
        if not secret or not signature:
            return False
        expected = hmac.new(secret.encode(), body, hashlib.sha512).hexdigest()
        return hmac.compare_digest(expected, signature)