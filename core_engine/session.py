"""
Session represents a single immutable simulation run.

It is a finite-state machine and evidence ledger.
Only the SimulationEngine is allowed to mutate it.
"""

from enum import Enum
from typing import List, Any
import uuid

from core_engine.exceptions import InvalidStateError


class SessionState(Enum):
    CREATED = "created"
    ACTIVE = "active"
    HALTED = "halted"
    COMPLETED = "completed"


class Session:
    def __init__(self, industry: str, role: str):
        # Stable unique identifier for persistence
        self.id = int(uuid.uuid4().int >> 64)

        self._industry = industry
        self._role = role

        self._state = SessionState.CREATED
        self._time = 0

        self._decisions: List[Any] = []
        self._events: List[Any] = []

        # Cohort classification
        self._cohort_profile = None

    # -------------------------
    # State Management
    # -------------------------

    def start(self) -> None:
        if self._state != SessionState.CREATED:
            raise InvalidStateError("Session cannot be started twice")
        self._state = SessionState.ACTIVE

    def end(self) -> None:
        if self._state != SessionState.ACTIVE:
            raise InvalidStateError("Only active sessions can end")
        self._state = SessionState.COMPLETED

    def halt(self) -> None:
        if self._state != SessionState.ACTIVE:
            raise InvalidStateError("Only active sessions can be halted")
        self._state = SessionState.HALTED

    def is_active(self) -> bool:
        return self._state == SessionState.ACTIVE

    def can_step(self) -> bool:
        return self._state == SessionState.ACTIVE

    # -------------------------
    # Time Control
    # -------------------------

    def advance_time(self, delta: int) -> None:
        if not self.is_active():
            raise InvalidStateError("Cannot advance time on inactive session")
        if delta <= 0:
            raise InvalidStateError("Time delta must be positive")
        self._time += delta

    @property
    def current_time(self) -> int:
        return self._time

    # -------------------------
    # Evidence Recording
    # -------------------------

    def record_decision(self, decision) -> None:
        if not self.is_active():
            raise InvalidStateError("Cannot record decision on inactive session")
        self._decisions.append(decision)

    def record_event(self, event) -> None:
        if not self.is_active():
            raise InvalidStateError("Cannot record event on inactive session")
        self._events.append(event)

    # -------------------------
    # Cohort Assignment
    # -------------------------

    def assign_cohort(self, profile) -> None:
        if self._state != SessionState.CREATED:
            raise InvalidStateError(
                "Cohort must be assigned before session starts stepping"
            )
        self._cohort_profile = profile

    @property
    def cohort_profile(self):
        return self._cohort_profile

    # -------------------------
    # Read-Only Accessors
    # -------------------------

    @property
    def industry(self) -> str:
        return self._industry

    @property
    def role(self) -> str:
        return self._role

    @property
    def decisions(self) -> List:
        return list(self._decisions)

    @property
    def events(self) -> List:
        return list(self._events)

    @property
    def state(self) -> SessionState:
        return self._state

    # -------------------------
    # Persistence
    # -------------------------

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "industry": self._industry,
            "role": self._role,
            "state": self._state.value,
            "time": self._time,
            "decisions": self._decisions,
            "events": self._events,
            "cohort_profile": self._cohort_profile,
        }

    def restore(self, data: dict) -> None:
        self.id = data.get("id", self.id)
        self._industry = data.get("industry", self._industry)
        self._role = data.get("role", self._role)
        self._state = SessionState(data.get("state", "created"))
        self._time = data.get("time", 0)
        self._decisions = data.get("decisions", [])
        self._events = data.get("events", [])
        self._cohort_profile = data.get("cohort_profile", None)