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
    Executes a single simulation step:
    - evaluate rules
    - record decisions (guarded)
    - record events (guarded)
    - advance time
    """

    if not session.is_active():
        raise InvalidStateError("Cannot step inactive session")

    try:
        # -------------------------
        # 1. Evaluate rules → decisions
        # -------------------------
        proposed_decisions = self._evaluate_rules(session)

        recorded_titles = {
            d.get("title")
            for d in session.decisions
            if d.get("time") == session.current_time
        }

        decisions_recorded = 0
        MAX_DECISIONS_PER_STEP = 3

        for decision in proposed_decisions:
            if decisions_recorded >= MAX_DECISIONS_PER_STEP:
                break

            # Deduplicate by title per time step
            if decision.title in recorded_titles:
                continue

            session.record_decision({
                "decision_id": decision.decision_id,
                "title": decision.title,
                "description": decision.description,
            })

            recorded_titles.add(decision.title)
            decisions_recorded += 1

        # -------------------------
        # 2. Generate events (guarded)
        # -------------------------
        proposed_events = self._generate_events(session)

        recorded_events = {
            (e.get("event_type"), e.get("description"))
            for e in session.events
            if e.get("time") == session.current_time
        }

        for event in proposed_events:
            key = (event.event_type, event.description)

            # Prevent duplicate events per step
            if key in recorded_events:
                continue

            session.trigger_event({
                "event_type": event.event_type,
                "description": event.description,
                "severity": event.severity,
            })

            recorded_events.add(key)

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