"""
Decision Models

A Decision represents an intentional action derived from rules,
humans, or AI. Decisions do NOT mutate session state directly.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from enum import Enum


class DecisionType(str, Enum):
    APPROVE_WORK = "approve_work"
    REJECT_WORK = "reject_work"
    ASSIGN_RESOURCE = "assign_resource"
    REALLOCATE_RESOURCE = "reallocate_resource"
    ESCALATE = "escalate"
    DELAY = "delay"
    CANCEL = "cancel"
    COMPLETE_WORK = "complete_work"


@dataclass(frozen=True)
class Decision:
    """
    Immutable decision object.
    """

    decision_type: DecisionType
    target_id: str
    payload: Dict[str, Any] = field(default_factory=dict)
    reason: Optional[str] = None
    issued_by: Optional[str] = None  # human, role, rule, or AI

    def validate(self) -> None:
        """
        Validates decision structure only.
        Raises ValueError if invalid.
        """

        if not self.target_id:
            raise ValueError("Decision must reference a target_id")

        if not isinstance(self.payload, dict):
            raise ValueError("Decision payload must be a dictionary")

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize decision for storage, replay, or inspection.
        """
        return {
            "decision_type": self.decision_type.value,
            "target_id": self.target_id,
            "payload": self.payload,
            "reason": self.reason,
            "issued_by": self.issued_by,
        }