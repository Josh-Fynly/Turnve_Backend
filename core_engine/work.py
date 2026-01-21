"""
Turnve Core Simulation Engine – Work

Defines how work enters the system, progresses, and completes.

Design principles:
- Work is executed, not answered
- Work consumes time and resources
- Work follows strict, realistic state transitions
- No industry-specific logic
"""

from dataclasses import dataclass, field
from typing import Optional, Dict
import uuid

from .exceptions import WorkError, InvalidWorkTransitionError


# -------------------------
# Work Item
# -------------------------

@dataclass
class WorkItem:
    """
    A unit of work inside a simulation.

    This represents real operational work:
    - It requires effort
    - It consumes resources
    - It progresses over time
    """
    id: str
    title: str
    description: str

    estimated_effort: int                  # abstract time units
    required_resources: Dict[str, int]

    priority: int                          # lower = more urgent
    created_at: int                        # simulation time

    started_at: Optional[int] = None
    completed_at: Optional[int] = None
    status: str = field(default="pending")  # pending | in_progress | blocked | completed

    def is_active(self) -> bool:
        return self.status in {"in_progress", "blocked"}

    def is_completed(self) -> bool:
        return self.status == "completed"


# -------------------------
# Work Factory
# -------------------------

class WorkFactory:
    """
    Responsible for creating valid work items.

    Industry plugins define WHAT work exists.
    The core engine defines HOW work behaves.
    """

    @staticmethod
    def create(
        title: str,
        description: str,
        estimated_effort: int,
        required_resources: Dict[str, int],
        priority: int,
        created_at: int,
    ) -> WorkItem:

        if not title:
            raise WorkError("Work title is required")

        if estimated_effort <= 0:
            raise WorkError("Work must require positive effort")

        if priority < 0:
            raise WorkError("Priority must be zero or greater")

        if created_at < 0:
            raise WorkError("Work creation time cannot be negative")

        return WorkItem(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            estimated_effort=estimated_effort,
            required_resources=required_resources or {},
            priority=priority,
            created_at=created_at,
        )


# -------------------------
# Work State Machine
# -------------------------

class WorkStateMachine:
    """
    Controls legal transitions of work state.

    Prevents unrealistic behavior such as:
    - Completing work that never started
    - Restarting completed work
    """

    VALID_TRANSITIONS = {
        "pending": {"in_progress"},
        "in_progress": {"blocked", "completed"},
        "blocked": {"in_progress"},
        "completed": set(),
    }

    @staticmethod
    def transition(
        work: WorkItem,
        new_state: str,
        current_time: int,
    ) -> None:

        if new_state not in WorkStateMachine.VALID_TRANSITIONS:
            raise WorkError(f"Unknown work state: {new_state}")

        allowed = WorkStateMachine.VALID_TRANSITIONS.get(work.status, set())

        if new_state not in allowed:
            raise InvalidWorkTransitionError(
                f"Illegal work transition from '{work.status}' to '{new_state}'"
            )

        if current_time < work.created_at:
            raise WorkError("Work cannot transition before it is created")

        work.status = new_state

        if new_state == "in_progress":
            if work.started_at is not None:
                raise WorkError("Work has already been started")
            work.started_at = current_time

        if new_state == "completed":
            if work.started_at is None:
                raise WorkError("Cannot complete work that never started")
            work.completed_at = current_time