"""
Decision represents a proposed action produced by rules.

Decisions are validated, recorded, but NOT executed.
"""

from enum import Enum
from typing import Optional

from core_engine.exceptions import InvalidStateError


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Decision:
    def __init__(
        self,
        *,
        decision_id: str,
        title: str,
        description: str,
        actor_role: str,
        time: int,
        risk_level: RiskLevel,
        confidence: float,
    ):
        self.decision_id = decision_id
        self.title = title
        self.description = description
        self.actor_role = actor_role
        self.time = time
        self.risk_level = risk_level
        self.confidence = confidence

        self._validated = False

    # -------------------------
    # Validation
    # -------------------------

    def validate(self) -> None:
        if self._validated:
            raise InvalidStateError("Decision already validated")

        if not self.decision_id:
            raise InvalidStateError("Decision must have an ID")

        if not self.title:
            raise InvalidStateError("Decision must have a title")

        if not self.actor_role:
            raise InvalidStateError("Decision must specify actor role")

        if self.time < 0:
            raise InvalidStateError("Decision time cannot be negative")

        if not (0.0 <= self.confidence <= 1.0):
            raise InvalidStateError("Decision confidence must be between 0 and 1")

        self._validated = True

    # -------------------------
    # Read-Only Properties
    # -------------------------

    @property
    def validated(self) -> bool:
        return self._validated