# app/database/payments_models.py
from typing import Optional
from datetime import datetime
from sqlalchemy import Index, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, DateTime, Text
from app.core.database import Base
from app.core.utils import utc_now

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reference: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)  # stored in kobo/cents
    currency: Mapped[Optional[str]] = mapped_column(String(10), default="NGN")
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending", index=True)
    gateway_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False, index=True)

    user = relationship("User", back_populates="transactions", lazy="joined")

    __table_args__ = (
        Index("idx_transaction_reference_status", "reference", "status"),
        Index("idx_transaction_user_status", "user_id", "status"),
    )


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="inactive", index=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    auto_renew: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False, index=True)

    user = relationship("User", back_populates="subscriptions")

    __table_args__ = (
        Index("idx_subscription_user_status", "user_id", "status"),
        Index("idx_subscription_plan_status", "plan_id", "status"),
    )