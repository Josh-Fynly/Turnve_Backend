# app/api/payments.py
from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.services.paystack_service import PaystackService
from app.database.payments_models import Transaction
from app.database.user_models import User
from datetime import datetime
import json

router = APIRouter(prefix="/payments", tags=["payments"])
paystack = PaystackService()


# Dependency to get db session
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


@router.post("/paystack/initialize")
async def paystack_init(email: str, amount: float, plan_id: str | None = None, db: AsyncSession = Depends(get_db)):
    """
    Initialize a Paystack transaction.
    amount is in NGN (e.g., 1000.50) — converted to kobo below.
    """
    amount_kobo = int(round(float(amount) * 100))
    metadata = {"plan_id": plan_id} if plan_id else {}
    callback_url = settings.paystack_callback_url or getattr(settings, "PAYSTACK_CALLBACK_URL", None)

    result = await paystack.initialize_transaction(email=email, amount_kobo=amount_kobo, metadata=metadata, callback_url=callback_url)
    ref = result.get("data", {}).get("reference")
    currency = result.get("data", {}).get("currency", "NGN")

    # Persist pending transaction
    tx = Transaction(
        reference=ref,
        user_id=None,
        amount=amount_kobo,
        currency=currency,
        status="pending"
    )
    db.add(tx)
    await db.commit()
    await db.refresh(tx)

    return {
        "reference": ref,
        "authorization_url": result.get("data", {}).get("authorization_url"),
        "access_code": result.get("data", {}).get("access_code"),
        "status": "initialized",
    }


@router.get("/paystack/verify/{reference}")
async def paystack_verify(reference: str, db: AsyncSession = Depends(get_db)):
    # Local DB check
    q = await db.execute(select(Transaction).where(Transaction.reference == reference))
    tx = q.scalars().first()

    # Remote verify
    resp = await paystack.verify_transaction(reference)
    data = resp.get("data", {})
    status = data.get("status")

    if not tx:
        # create if not present
        tx = Transaction(
            reference=reference,
            user_id=None,
            amount=int(data.get("amount", 0)),
            currency=data.get("currency", "NGN"),
            status=status or "unknown",
            gateway_response=json.dumps(data),
            paid_at=datetime.utcfromtimestamp(data.get("paid_at")) if data.get("paid_at") else None
        )
        db.add(tx)
    else:
        tx.status = status or tx.status
        tx.gateway_response = json.dumps(data)
        if data.get("paid_at"):
            tx.paid_at = datetime.utcfromtimestamp(data.get("paid_at"))

    await db.commit()
    return {"status": tx.status, "reference": tx.reference}


@router.post("/paystack/webhook")
async def paystack_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    body = await request.body()
    signature = request.headers.get("x-paystack-signature")
    if not paystack.verify_webhook_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    event = payload.get("event")
    data = payload.get("data", {})

    if event == "charge.success":
        reference = data.get("reference")
        q = await db.execute(select(Transaction).where(Transaction.reference == reference))
        tx = q.scalars().first()

        if not tx:
            tx = Transaction(
                reference=reference,
                user_id=None,
                amount=int(data.get("amount", 0)),
                currency=data.get("currency", "NGN"),
                status="success",
                gateway_response=json.dumps(data),
            )
            db.add(tx)
        else:
            tx.status = "success"
            tx.gateway_response = json.dumps(data)

        # Link to user if email exists
        customer_email = data.get("customer", {}).get("email")
        if customer_email:
            q2 = await db.execute(select(User).where(User.email == customer_email))
            user = q2.scalars().first()
            if user:
                tx.user_id = user.id
                # (optionally unlock product / grant access here)

        await db.commit()
        return {"status": "ok"}

    return {"status": "ignored"}