"""
Turnve Core Simulation Engine – Engine

The Engine is the authoritative orchestrator of a simulation session.

Design principles:
- Centralized control
- Deterministic execution
- Industry-agnostic
- No AI, no UI, no scoring
"""

from typing import Optional

from .session import Session
from .time import SimulationClock
from .work import WorkItem, WorkStateMachine
from .resource import ResourcePool
from .decision import Decision
from .exceptions import (
    EngineStateError,
    SessionNotStartedError,
    InvalidWorkTransitionError,
)


class SimulationEngine:
    """
    The single source of truth for running a simulation.

    All state mutations must pass through this engine.
    """

    def __init__(self, session: Session):
        self.session = session

        self.clock = SimulationClock(start_time=session.current_time)
        self.resources = ResourcePool()

        self._running: bool = False

    # -------------------------
    # Lifecycle
    # -------------------------

    def start(self) -> None:
        if self._running:
            raise EngineStateError("Engine already running")

        self.session.start()
        self.clock.start()

        self._running = True

        self.session.log_evidence({
            "type": "engine_started",
        })

    def stop(self) -> None:
        if not self._running:
            raise EngineStateError("Engine not running")

        self.clock.stop()
        self.session.end()

        self._running = False

        self.session.log_evidence({
            "type": "engine_stopped",
        })

    def is_running(self) -> bool:
        return self._running

    # -------------------------
    # Time control
    # -------------------------

    def advance_time(self, delta: int, reason: str) -> None:
        if not self._running:
            raise SessionNotStartedError("Engine is not running")

        self.clock.advance(delta=delta, reason=reason)
        self.session.current_time = self.clock.now

        self.session.log_evidence({
            "type": "time_advanced",
            "delta": delta,
            "reason": reason,
        })

    # -------------------------
    # Work orchestration
    # -------------------------

    def register_work(self, work: WorkItem) -> None:
        if not self._running:
            raise SessionNotStartedError("Engine is not running")

        self.session.register_work(work.id, {
            "work": work,
            "status": work.status,
        })

        self.session.log_evidence({
            "type": "work_registered",
            "work_id": work.id,
            "title": work.title,
        })

    def start_work(self, work: WorkItem) -> None:
        if not self._running:
            raise SessionNotStartedError("Engine is not running")

        # Allocate required resources
        self.resources.allocate(work.required_resources)

        WorkStateMachine.transition(
            work=work,
            new_state="in_progress",
            current_time=self.session.current_time,
        )

        self.session.log_evidence({
            "type": "work_started",
            "work_id": work.id,
        })

    def block_work(self, work: WorkItem, reason: str) -> None:
        WorkStateMachine.transition(
            work=work,
            new_state="blocked",
            current_time=self.session.current_time,
        )

        self.session.log_evidence({
            "type": "work_blocked",
            "work_id": work.id,
            "reason": reason,
        })

    def complete_work(self, work: WorkItem) -> None:
        WorkStateMachine.transition(
            work=work,
            new_state="completed",
            current_time=self.session.current_time,
        )

        # Release resources
        self.resources.release(work.required_resources)

        self.session.complete_work(work.id)

        self.session.log_evidence({
            "type": "work_completed",
            "work_id": work.id,
        })

    # -------------------------
    # Decisions
    # -------------------------

    def apply_decision(self, decision: Decision, option_id: str) -> None:
        if not self._running:
            raise SessionNotStartedError("Engine is not running")

        if not decision.is_available(self.session.current_time):
            raise EngineStateError("Decision is no longer available")

        decision.make(option_id=option_id, session=self.session)

        self.session.log_evidence({
            "type": "decision_applied",
            "decision_id": decision.decision_id,
            "option_id": option_id,
        })