"""
Tech Industry Rules

Rules observe the session state and propose decisions.
They DO NOT mutate state or execute actions.
"""

from typing import List
import uuid

from core_engine.decision import Decision, RiskLevel
from core_engine.session import Session


# -------------------------
# Public API (Engine Hook)
# -------------------------

def evaluate_rules(session: Session) -> List[Decision]:
    """
    Evaluates current session state and proposes decisions.
    """
    decisions: List[Decision] = []

    # Rule 1: Unstarted high-priority work
    decisions.extend(_prioritization_rule(session))

    # Rule 2: Overloaded coordination (JPM-specific)
    decisions.extend(_coordination_risk_rule(session))

    return decisions


# -------------------------
# Rule Implementations
# -------------------------

def _prioritization_rule(session: Session) -> List[Decision]:
    """
    If there are pending high-priority work items,
    propose a prioritization decision.
    """
    decisions = []

    pending_work = [
        w for w in session.work_items()
        if w.status == "pending" and w.priority == 0
    ]

    if pending_work:
        decisions.append(
            Decision(
                decision_id=str(uuid.uuid4()),
                title="Prioritize urgent work",
                description=(
                    "There are high-priority tasks pending. "
                    "Decide whether to start immediately or re-sequence work."
                ),
                actor_role=session.role,
                time=session.current_time(),
                risk_level=RiskLevel.MEDIUM,
                confidence=0.7,
            )
        )

    return decisions


def _coordination_risk_rule(session: Session) -> List[Decision]:
    """
    JPM-focused rule:
    If many tasks are in-progress simultaneously,
    surface a coordination risk decision.
    """
    decisions = []

    in_progress = [
        w for w in session.work_items()
        if w.status == "in_progress"
    ]

    if len(in_progress) >= 4:
        decisions.append(
            Decision(
                decision_id=str(uuid.uuid4()),
                title="Address coordination risk",
                description=(
                    "Multiple tasks are running in parallel. "
                    "Decide whether to pause work, reassign focus, "
                    "or accept coordination risk."
                ),
                actor_role=session.role,
                time=session.current_time(),
                risk_level=RiskLevel.HIGH,
                confidence=0.6,
            )
        )

    return decisions