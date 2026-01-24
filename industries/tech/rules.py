"""
Tech Industry Rules

Rules evaluate session state and completed work to determine:
- which events should fire
- which categories of work are unlocked
"""

from typing import List

from industries.tech.events import (
    architecture_finalized_event,
    deployment_strategy_approved_event,
)
from core_engine.event import Event


# -------------------------
# Rule: Repository Required
# -------------------------

def repo_required_for_engineering(session) -> bool:
    """
    Engineering work requires a connected repository.
    """
    return session.flags.get("repo_connected", False)


# -------------------------
# Rule: Architecture Before Build
# -------------------------

def architecture_required_before_build(session) -> bool:
    """
    Prevents implementation work before architecture is finalized.
    """
    return session.flags.get("architecture_ready", False)


# -------------------------
# Rule: Deployment Requires Build Completion
# -------------------------

def deployment_requires_build(session) -> bool:
    """
    Deployment is allowed only after implementation milestones exist.
    """
    return session.evidence.has_category("work_completion")


# -------------------------
# Rule: JPM Phase Approval
# -------------------------

def jpm_approval_required(session, phase: str) -> bool:
    """
    Junior Project Manager must approve phase transitions.
    """
    approvals = session.flags.get("jpm_approvals", set())
    return phase in approvals


# -------------------------
# Rule: Evaluate Phase Transitions
# -------------------------

def evaluate_phase_events(session) -> List[Event]:
    """
    Determines which phase-related events should be triggered
    based on accumulated evidence and flags.
    """

    events: List[Event] = []

    # Architecture finalized
    if (
        not session.flags.get("architecture_ready")
        and session.evidence.has_category("architecture")
    ):
        events.append(architecture_finalized_event())

    # Deployment strategy approved
    if (
        session.flags.get("architecture_ready")
        and not session.flags.get("deployment_ready")
        and session.evidence.has_category("delivery")
    ):
        events.append(deployment_strategy_approved_event())

    return events