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
        """
        industry_name: e.g. 'tech'
        """
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
        Executes a single simulation step:
        - evaluate rules
        - record decisions
        - record events
        - advance time
        """

        if not session.is_active():
            raise InvalidStateError("Cannot step inactive session")

        try:
            # -------------------------
            # 1. Evaluate rules → decisions
            # -------------------------
            decisions = self._evaluate_rules(session)

            for decision in decisions:
                # MVP: record only, no execution layer yet
                session.record_decision({
                    "decision_id": getattr(decision, "decision_id", None),
                    "title": getattr(decision, "title", None),
                    "description": getattr(decision, "description", None),
                })

            # -------------------------
            # 2. Generate events
            # -------------------------
            events = self._generate_events(session)

            for event in events:
                session.trigger_event({
                    "event_type": getattr(event, "event_type", None),
                    "description": getattr(event, "description", None),
                    "severity": getattr(event, "severity", None),
                })

            # -------------------------
            # 3. Advance time
            # -------------------------
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
        Generates initial work.
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