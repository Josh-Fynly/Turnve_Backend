"""
Simulation Session

Authoritative state container for a Turnve simulation.
All state mutations MUST pass through this object.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from uuid import uuid4
from datetime import datetime

from core_engine.exceptions import (
    InvalidStateError,
    SimulationHalt,
)


@dataclass
class Session:
    # -------------------------
    # Identity & Metadata
    # -------------------------

    session_id: str = field(default_factory=lambda: str(uuid4()))
    industry: str = ""
    role: str = ""

    # -------------------------
    # Lifecycle
    # -------------------------

    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    _active: bool = False

    # -------------------------
    # Time
    # -------------------------

    current_tick: int = 0

    # -------------------------
    # Core State
    # -------------------------

    active_work: Dict[str, Any] = field(default_factory=dict)
    completed_work: Dict[str, Any] = field(default_factory=dict)

    events: List[Any] = field(default_factory=list)
    decisions: List[Any] = field(default_factory=list)
    evidence: List[Dict[str, Any]] = field(default_factory=list)

    # -------------------------
    # Structured Context
    # -------------------------

    flags: Dict[str, bool] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)

    # =========================
    # Lifecycle Control
    # =========================

    def start(self) -> None:
        if self._active:
            raise InvalidStateError("Session already started")

        if self.ended_at is not None:
            raise InvalidStateError("Cannot restart ended session")

        self.started_at = datetime.utcnow()
        self._active = True

        self._record_evidence(
            "session_started",
            {"started_at": self.started_at.isoformat()},
        )

    def end(self) -> None:
        if not self._active:
            raise InvalidStateError("Cannot end inactive session")

        self.ended_at = datetime.utcnow()
        self._active = False

        self._record_evidence(
            "session_ended",
            {"ended_at": self.ended_at.isoformat()},
        )

    def is_active(self) -> bool:
        return self._active

    # =========================
    # Time Control
    # =========================

    def advance_time(self, ticks: int = 1) -> None:
        if not self._active:
            raise InvalidStateError("Cannot advance time on inactive session")

        if ticks <= 0:
            raise InvalidStateError("Time advancement must be positive")

        self.current_tick += ticks

        self._record_evidence(
            "time_advanced",
            {"current_tick": self.current_tick},
        )

    # =========================
    # Work Management
    # =========================

    def add_work(self, work_id: str, work: Any) -> None:
        self._assert_active()

        if work_id in self.active_work or work_id in self.completed_work:
            raise InvalidStateError(f"Work '{work_id}' already exists")

        self.active_work[work_id] = work

        self._record_evidence(
            "work_added",
            {"work_id": work_id},
        )

    def complete_work(self, work_id: str) -> None:
        self._assert_active()

        if work_id not in self.active_work:
            raise InvalidStateError(f"Work '{work_id}' not found")

        work = self.active_work.pop(work_id)
        self.completed_work[work_id] = work

        self._record_evidence(
            "work_completed",
            {"work_id": work_id},
        )

    # =========================
    # Decisions & Events
    # =========================

    def record_decision(self, decision: Any) -> None:
        self._assert_active()
        self.decisions.append(decision)

        self._record_evidence(
            "decision_recorded",
            {"decision": getattr(decision, "to_dict", lambda: decision)()},
        )

    def record_event(self, event: Any) -> None:
        self._assert_active()
        self.events.append(event)

        self._record_evidence(
            "event_recorded",
            {"event": str(event)},
        )

    # =========================
    # Evidence (Append-Only)
    # =========================

    def _record_evidence(self, event_type: str, payload: Dict[str, Any]) -> None:
        self.evidence.append({
            "tick": self.current_tick,
            "type": event_type,
            "payload": payload,
            "timestamp": datetime.utcnow().isoformat(),
        })

    # =========================
    # Snapshot (Read-Only)
    # =========================

    def snapshot(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "industry": self.industry,
            "role": self.role,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "current_tick": self.current_tick,
            "active_work": dict(self.active_work),
            "completed_work": dict(self.completed_work),
            "events": list(self.events),
            "decisions": list(self.decisions),
            "evidence": list(self.evidence),
            "flags": dict(self.flags),
            "metrics": dict(self.metrics),
            "active": self._active,
        }

    # =========================
    # Internal Guards
    # =========================

    def _assert_active(self) -> None:
        if not self._active:
            raise SimulationHalt("Session is not active")