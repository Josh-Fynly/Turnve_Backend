"""
Tech Industry Rules

Rules observe the current session state and propose decisions.
They do NOT mutate state, generate work, or trigger events.
"""

from typing import List
import uuid

from core_engine.decision import Decision
from core_engine.session import Session


# -------------------------
# Public Engine Hook
# -------------------------

def evaluate_rules(session: Session) -> List[Decision]:
    """
    Entry point called by the SimulationEngine.
    """
    decisions: List[Decision] = []

    decisions.extend(_prioritization_pressure_rule(session))
    decisions.extend(_coordination_overload_rule(session))
    decisions.extend(_stalled_work_rule(session))

    return decisions


# -------------------------
# Rule Implementations
# -------------------------

def _prioritization_pressure_rule(session: Session) -> List[Decision]:
    """
    If multiple high-effort work items are pending,
    surface a prioritization decision.
    """
    decisions = []

    pending = [
        w for w in session.work_items.values()
        if w.get("status") == "pending"
    ]

    high_effort = [
        w for w in pending
        if w.get("estimated_effort", 0) >= 5
    ]

    if len(high_effort) >= 2:
        decisions.append(
            Decision(
                decision_id=str(uuid.uuid4()),
                title="Prioritize major work items",
                description=(
                    "Multiple high-effort work items are pending. "
                    "Decide which to focus on first and which to defer."
                ),
                actor_role=session.role,
                time=session.current_time,
            )
        )

    return decisions


def _coordination_overload_rule(session: Session) -> List[Decision]:
    """
    JPM-focused rule.
    If too many tasks are in progress at once,
    coordination risk increases.
    """
    decisions = []

    in_progress = [
        w for w in session.work_items.values()
        if w.get("status") == "in_progress"
    ]

    if len(in_progress) >= 4:
        decisions.append(
            Decision(
                decision_id=str(uuid.uuid4()),
                title="Address coordination overload",
                description=(
                    "Several tasks are running in parallel. "
                    "Decide whether to pause work, reassign focus, "
                    "or accept coordination risk."
                ),
                actor_role=session.role,
                time=session.current_time,
            )
        )

    return decisions


def _stalled_work_rule(session: Session) -> List[Decision]:
    """
    If work has been pending for too long without progress,
    surface a decision to unblock or re-scope.
    """
    decisions = []

    stalled = [
        w for w in session.work_items.values()
        if w.get("status") == "pending"
        and (session.current_time - w.get("created_at", 0)) >= 3
    ]

    if stalled:
        decisions.append(
            Decision(
                decision_id=str(uuid.uuid4()),
                title="Unblock stalled work",
                description=(
                    "Some work items have been pending without progress. "
                    "Decide whether to unblock, deprioritize, or remove them."
                ),
                actor_role=session.role,
                time=session.current_time,
            )
        )

    return decisions