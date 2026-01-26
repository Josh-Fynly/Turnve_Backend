"""
Session represents a single immutable simulation run.

It is a finite-state machine and evidence ledger.
Only the SimulationEngine is allowed to mutate it.
"""

from enum import Enum
from typing import List

from core_engine.exceptions import InvalidStateError


class SessionState(Enum):
    CREATED = "created"
    ACTIVE = "active"
    HALTED = "halted"
    COMPLETED = "completed"


class Session:
    def __init__(self, industry: str, role: str):
        self._industry = industry
        self._role = role

        self._state = SessionState.CREATED
        self._time = 0

        self._decisions: List = []
        self._events: List = []

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