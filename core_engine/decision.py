"""
Decision & Rule System

Defines how decisions are produced by rules and applied by the engine.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional


# -------------------------
# Decision Object
# -------------------------

@dataclass(frozen=True)
class Decision:
    """
    Represents an actionable outcome produced by a rule.

    The engine applies decisions.
    Rules only propose them.
    """
    type: str
    payload: dict
    reason: str
    source: str = "system"  # system | human | ai


# -------------------------
# Rule Interface
# -------------------------

class DecisionRule(ABC):
    """
    Base class for all decision rules.

    Rules:
    - Observe session state
    - Decide if they apply
    - Propose a decision (or None)
    """

    name: str = "UnnamedRule"

    def applies(self, session) -> bool:
        """
        Lightweight check.
        Must not mutate state.
        """
        return True

    @abstractmethod
    def evaluate(self, session) -> Optional[Decision]:
        """
        Evaluate the rule and optionally return a Decision.

        Must not mutate session.
        """
        raise NotImplementedError