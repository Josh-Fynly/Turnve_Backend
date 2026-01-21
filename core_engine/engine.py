"""
Turnve Core Simulation Engine – Engine

The Engine is the orchestrator of a simulation session.
It advances time, executes work, applies decisions, and triggers events.

Design principles:
- Deterministic
- Industry-agnostic
- No AI, no UI
- All state changes go through here
"""

from typing import Optional

from .session import Session
from .work import WorkItem, WorkStateMachine
from .exceptions import (
    SessionNotStartedError,
    EngineStateError,
)


class SimulationEngine:
    """
    The authoritative executor of simulation logic.
    """

    def __init__(self, session: Session):
        if not isinstance(session, Session):
            raise TypeError("Engine requires a valid Session")

        self.session = session

    # -------------------------
    # Public API
    # -------------------------

    def start(self) -> None:
        """
        Starts the simulation session.
        """
        self.session.start()

    def step(self, time_delta: int, reason: str) -> None:
        """
        Advances the simulation by one step.

        A step represents:
        - time advancing
        - work progressing
        - events triggering
        """
        self._ensure_active()

        # 1. Advance time
        self.session.time.advance(time_delta, reason)

        # 2. Progress work
        self._progress_work()

        # 3. Trigger scheduled events (if any)
        self._trigger_events()

    def end(self) -> None:
        """
        Ends the simulation session.
        """
        self.session.end()

    # -------------------------
    # Internal mechanics
    # -------------------------

    def _ensure_active(self) -> None:
        if not self.session.is_active():
            raise SessionNotStartedError("Simulation session is not active")

    def _progress_work(self) -> None:
        """
        Advances in-progress work based on time and resources.
        """
        for work in self.session.work_items.values():

            if work.status != "in_progress":
                continue

            # Reduce remaining effort
            work.estimated_effort -= 1

            self.session.log({
                "type": "work_progressed",
                "work_id": work.id,
                "remaining_effort": work.estimated_effort,
            })

            # Complete work if effort exhausted
            if work.estimated_effort <= 0:
                WorkStateMachine.transition(
                    work,
                    new_state="completed",
                    current_time=self.session.time.now
                )

                self.session.log({
                    "type": "work_completed",
                    "work_id": work.id,
                })

    def _trigger_events(self) -> None:
        """
        Triggers pending events registered in the session.
        """
        while self.session.events:
            event = self.session.events.pop(0)

            self.session.log({
                "type": "event_triggered",
                "description": event.description,
            })

            event.trigger(self.session)