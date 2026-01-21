"""
Turnve Core Simulation Engine – Session

A Session represents a single, continuous simulation run.
It is the authoritative owner of time, resources, work, events, and evidence.

Design principles:
- Deterministic
- Auditable
- Engine-only (no UI, no AI, no industry logic)
"""

from typing import Dict, List, Optional
from uuid import UUID, uuid4
from datetime import datetime

from .time import SimulationClock
from .resource import ResourcePool
from .work import WorkItem
from .decision import Decision
from .event import Event
from .exceptions import (
    SessionNotStartedError,
    SessionAlreadyEndedError,
    EngineStateError,
)


class Session:
    """
    Authoritative container for a simulation run.
    """

    def __init__(
        self,
        industry: str,
        role: str,
        actors: Optional[List[str]] = None,
        session_id: Optional[UUID] = None,
    ):
        self.id: UUID = session_id or uuid4()

        self.industry = industry
        self.role = role
        self.actors = actors or []

        self.started_at: Optional[datetime] = None
        self.ended_at: Optional[datetime] = None
        self._active: bool = False

        # Core systems
        self.time = SimulationClock(start_time=0)
        self.resources = ResourcePool()

        # State containers
        self.work_items: Dict[str, WorkItem] = {}
        self.decisions: List[Decision] = []
        self.events: List[Event] = []

        # Evidence log (append-only)
        self.evidence: List[dict] = []

    # -------------------------
    # Lifecycle
    # -------------------------

    def start(self) -> None:
        if self._active:
            raise EngineStateError("Session already started")

        self.started_at = datetime.utcnow()
        self._active = True

        self.log({
            "type": "session_started",
            "industry": self.industry,
            "role": self.role,
        })

    def end(self) -> None:
        if not self._active:
            raise SessionNotStartedError("Session not active")

        self.ended_at = datetime.utcnow()
        self._active = False

        self.log({
            "type": "session_ended",
        })

    def is_active(self) -> bool:
        return self._active

    # -------------------------
    # Work
    # -------------------------

    def register_work(self, work: WorkItem) -> None:
        if not self._active:
            raise SessionNotStartedError("Session not active")

        self.work_items[work.id] = work

        self.log({
            "type": "work_registered",
            "work_id": work.id,
            "title": work.title,
        })

    # -------------------------
    # Decisions & Events
    # -------------------------

    def register_decision(self, decision: Decision) -> None:
        if not self._active:
            raise SessionNotStartedError("Session not active")

        self.decisions.append(decision)

    def trigger_event(self, event: Event) -> None:
        if not self._active:
            raise SessionNotStartedError("Session not active")

        self.events.append(event)
        event.trigger(self)

    # -------------------------
    # Evidence
    # -------------------------

    def log(self, record: dict) -> None:
        """
        Append-only evidence log.
        """
        self.evidence.append({
            **record,
            "time": self.time.now,
            "session_id": str(self.id),
        })

    # -------------------------
    # Snapshot
    # -------------------------

    def snapshot(self) -> dict:
        return {
            "session_id": str(self.id),
            "industry": self.industry,
            "role": self.role,
            "actors": self.actors,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "time": self.time.now,
            "resources": self.resources.snapshot(),
            "work_items": list(self.work_items.keys()),
            "decisions": [d.decision_id for d in self.decisions],
            "events": [e.description for e in self.events],
            "evidence_count": len(self.evidence),
            "active": self._active,
        }