"""
Simulation Session

Holds all mutable state for a simulation run.
Only the engine is allowed to mutate this object.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
from uuid import uuid4
from datetime import datetime


@dataclass
class Session:
    """
    Represents a single simulation instance.
    """

    # Identity
    session_id: str = field(default_factory=lambda: str(uuid4()))
    industry: str = ""
    role: str = ""

    # Time
    current_tick: int = 0
    started_at: datetime = field(default_factory=datetime.utcnow)

    # State containers
    active_work: Dict[str, Any] = field(default_factory=dict)
    completed_work: Dict[str, Any] = field(default_factory=dict)

    events: List[Any] = field(default_factory=list)
    decisions: List[Any] = field(default_factory=list)
    evidence: List[Any] = field(default_factory=list)

    # Metadata
    context: Dict[str, Any] = field(default_factory=dict)

    # -------------------------
    # Read-only helpers
    # -------------------------

    def snapshot(self) -> dict:
        """
        Immutable snapshot of the current session state.
        Safe for rules, AI, and UI.
        """
        return {
            "session_id": self.session_id,
            "industry": self.industry,
            "role": self.role,
            "current_tick": self.current_tick,
            "active_work": dict(self.active_work),
            "completed_work": dict(self.completed_work),
            "events": list(self.events),
            "decisions": list(self.decisions),
            "evidence": list(self.evidence),
            "context": dict(self.context),
        }

    # -------------------------
    # Mutation methods
    # (ENGINE ONLY)
    # -------------------------

    def advance_time(self, ticks: int = 1) -> None:
        self.current_tick += ticks

    def add_work(self, work_id: str, work: Any) -> None:
        self.active_work[work_id] = work

    def complete_work(self, work_id: str) -> None:
        work = self.active_work.pop(work_id, None)
        if work is not None:
            self.completed_work[work_id] = work

    def record_event(self, event: Any) -> None:
        self.events.append(event)

    def record_decision(self, decision: Any) -> None:
        self.decisions.append(decision)

    def record_evidence(self, evidence: Any) -> None:
        self.evidence.append(evidence)