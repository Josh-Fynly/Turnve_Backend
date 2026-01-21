from dataclasses import dataclass, field
from typing import Optional, Dict
import uuid


class WorkError(Exception):
    pass


@dataclass
class WorkItem:
    """
    A unit of work entering the simulation.

    This is NOT a task to be 'answered'.
    This is work that must be executed under constraints.
    """
    id: str
    title: str
    description: str

    estimated_effort: int          # time units required
    required_resources: Dict[str, int]

    priority: int                  # lower = more urgent
    created_at: int                # simulation time

    started_at: Optional[int] = None
    completed_at: Optional[int] = None
    status: str = field(default="pending")  # pending | in_progress | blocked | completed


class WorkFactory:
    """
    Responsible for creating work items.
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
        created_at: int
    ) -> WorkItem:

        if estimated_effort <= 0:
            raise WorkError("Work must require positive effort")

        if priority < 0:
            raise WorkError("Priority must be zero or greater")

        return WorkItem(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            estimated_effort=estimated_effort,
            required_resources=required_resources,
            priority=priority,
            created_at=created_at
        )


class WorkStateMachine:
    """
    Controls legal transitions of work state.
    Prevents unrealistic behavior.
    """

    VALID_TRANSITIONS = {
        "pending": {"in_progress"},
        "in_progress": {"blocked", "completed"},
        "blocked": {"in_progress"},
        "completed": set()
    }

    @staticmethod
    def transition(work: WorkItem, new_state: str, current_time: int):
        allowed = WorkStateMachine.VALID_TRANSITIONS.get(work.status, set())

        if new_state not in allowed:
            raise WorkError(
                f"Illegal transition from {work.status} to {new_state}"
            )

        work.status = new_state

        if new_state == "in_progress":
            work.started_at = current_time

        if new_state == "completed":
            work.completed_at = current_time