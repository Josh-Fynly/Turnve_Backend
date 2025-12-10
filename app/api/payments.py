from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.paystack_service import PaystackClient
from app.database.models.payment import Payment
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session


router = APIRouter(prefix="/payments", tags=["Payments"])


class PaymentInitRequest(BaseModel):
    email: str
    amount: int
    user_id: int


@router.post("/init")
async def init_payment(
    payload: PaymentInitRequest, session: AsyncSession = Depends(get_session)
):
    ps = PaystackClient()

    metadata = {"user_id": payload.user_id}

    result = await ps.initialize_transaction(
        email=payload.email,
        amount=payload.amount,
        metadata=metadata,
    )

    ref = result["data"]["reference"]

    payment = Payment(
        user_id=payload.user_id,
        email=payload.email,
        amount=payload.amount,
        reference=ref,
        status="pending"
    )

    session.add(payment)
    await session.commit()

    return result


@router.get("/verify/{reference}")
async def verify_payment(
    reference: str, session: AsyncSession = Depends(get_session)
):
    ps = PaystackClient()

    result = await ps.verify_transaction(reference)

    payment = (
        await session.execute(
            sa.select(Payment).where(Payment.reference == reference)
        )
    ).scalar_one_or_none()

    if not payment:
        raise HTTPException(404, "Payment not found")

    status = result["data"]["status"]
    payment.status = status

    await session.commit()

    return result