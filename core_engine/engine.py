"""
Turnve Core Simulation Engine

The Engine orchestrates simulation flow.
It is the ONLY authority allowed to mutate Session state.
"""

from typing import Any, List
import importlib

from core_engine.session import Session
from core_engine.exceptions import (
    SimulationHalt,
    InvalidStateError,
)


class SimulationEngine:
    """
    Orchestrates a single simulation session.
    """

    def __init__(self, industry_name: str):
        self.industry_name = industry_name
        self.industry = self._load_industry(industry_name)

    # -------------------------
    # Industry Loading
    # -------------------------

    def _load_industry(self, industry_name: str):
        try:
            return importlib.import_module(f"industries.{industry_name}")
        except ModuleNotFoundError as e:
            raise InvalidStateError(
                f"Industry '{industry_name}' could not be loaded"
            ) from e

    # -------------------------
    # Session Lifecycle
    # -------------------------

    def create_session(self, role: str) -> Session:
        session = Session(
            industry=self.industry_name,
            role=role,
        )
        session.start()
        self.initialize(session)
        return session

    def end_session(self, session: Session) -> None:
        if session.is_active():
            session.end()

    # -------------------------
    # Simulation Step
    # -------------------------

    def step(self, session: Session) -> None:
        """
        Executes a single simulation tick.
        Order is deterministic and enforced.
        """

        if not session.is_active():
            raise InvalidStateError("Cannot step inactive session")

        if not session.can_step():
            raise InvalidStateError("Session is not in a steppable state")

        try:
            current_tick = session.current_time()

            # 1. Evaluate rules → decisions
            decisions = self._evaluate_rules(session)
            decisions = sorted(decisions, key=lambda d: d.priority)

            # 2. Record decisions (execution deferred)
            for decision in decisions:
                decision.validate()
                decision.bind_time(current_tick)
                session.record_decision(decision)

            # 3. Generate events
            events = self._generate_events(session)
            events = sorted(events, key=lambda e: e.severity)

            for event in events:
                session.record_event(event)

            # 4. Advance time
            session.advance_time(1)

        except SimulationHalt:
            session.end()
            raise

    # -------------------------
    # Industry Hooks
    # -------------------------

    def initialize(self, session: Session) -> None:
        """
        Called exactly once after session start.
        Generates initial work canvas.
        """
        if hasattr(self.industry, "generate_initial_work"):
            self.industry.generate_initial_work(session)

    def _evaluate_rules(self, session: Session) -> List[Any]:
        if hasattr(self.industry, "evaluate_rules"):
            return self.industry.evaluate_rules(session)
        return []

    def _generate_events(self, session: Session) -> List[Any]:
        if hasattr(self.industry, "generate_events"):
            return self.industry.generate_events(session)
        return []