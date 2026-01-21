"""
Turnve Core Simulation Engine – Session

A Session represents a single, continuous simulation run.
It owns time, work, decisions, events, and evidence.

Design principles:
- Deterministic and auditable
- No UI, no AI, no industry-specific logic
- Safe for solo now, team-based later
"""

from typing import Dict, List, Optional
from uuid import UUID, uuid4
from datetime import datetime

from .exceptions import (
    SessionNotStartedError,
    SessionAlreadyEndedError,
    EngineStateError,
)


class Session:
    """
    A simulation session is the authoritative container for:
    - time progression
    - work items
    - decisions taken
    - events triggered
    - evidence generated

    A session is immutable once ended.
    """

    def __init__(
        self,
        industry: str,
        role: str,
        actors: Optional[List[str]] = None,
        session_id: Optional[UUID] = None,
    ):
        self.id: UUID = session_id or uuid4()

        self.industry: str = industry
        self.role: str = role

        self.actors: List[str] = actors or []

        self.started_at: Optional[datetime] = None
        self.ended_at: Optional[datetime] = None

        self.current_time: int = 0  # abstract simulation time units

        self.work_items: Dict[str, dict] = {}
        self.decisions: List[dict] = []
        self.events: List[dict] = []
        self.evidence: List[dict] = []

        self._active: bool = False

    # -------------------------
    # Lifecycle
    # -------------------------

    def start(self) -> None:
        if self._active:
            raise EngineStateError("Session already started")

        self.started_at = datetime.utcnow()
        self._active = True

    def end(self) -> None:
        if not self._active:
            raise SessionNotStartedError("Session has not started")

        self.ended_at = datetime.utcnow()
        self._active = False

    def is_active(self) -> bool:
        return self._active

    # -------------------------
    # Time control
    # -------------------------

    def advance_time(self, delta: int) -> None:
        if not self._active:
            raise SessionNotStartedError("Cannot advance time on inactive session")

        if delta <= 0:
            raise ValueError("Time delta must be positive")

        self.current_time += delta

    # -------------------------
    # Work management
    # -------------------------

    def register_work(self, work_id: str, payload: dict) -> None:
        if not self._active:
            raise SessionNotStartedError("Session must be active")

        self.work_items[work_id] = payload

    def complete_work(self, work_id: str) -> None:
        if work_id not in self.work_items:
            raise KeyError(f"Work item '{work_id}' not found")

        self.work_items[work_id]["completed"] = True

    # -------------------------
    # Decisions & events
    # -------------------------

    def record_decision(self, decision: dict) -> None:
        if not self._active:
            raise SessionNotStartedError("Cannot record decision")

        self.decisions.append({
            **decision,
            "time": self.current_time,
        })

    def trigger_event(self, event: dict) -> None:
        if not self._active:
            raise SessionNotStartedError("Cannot trigger event")

        self.events.append({
            **event,
            "time": self.current_time,
        })

    # -------------------------
    # Evidence
    # -------------------------

    def log_evidence(self, record: dict) -> None:
        """
        Evidence is append-only and immutable once written.
        """
        self.evidence.append({
            **record,
            "time": self.current_time,
            "session_id": str(self.id),
        })

    # -------------------------
    # Snapshot / export
    # -------------------------

    def snapshot(self) -> dict:
        """
        Returns a serializable snapshot of session state.
        Useful for persistence, replay, or certification.
        """
        return {
            "session_id": str(self.id),
            "industry": self.industry,
            "role": self.role,
            "actors": self.actors,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "current_time": self.current_time,
            "work_items": self.work_items,
            "decisions": self.decisions,
            "events": self.events,
            "evidence": self.evidence,
            "active": self._active,
        }