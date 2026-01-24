"""
Simulation Engine

Coordinates the execution of a simulation session.
This is the ONLY component allowed to mutate session state.
"""

from typing import Callable, List, Any
from core_engine.session import Session


class SimulationEngine:
    """
    Orchestrates simulation ticks.
    """

    def __init__(
        self,
        session: Session,
        work_generator: Callable[[Session], List[Any]],
        event_generator: Callable[[Session], List[Any]],
        rule_evaluator: Callable[[Session, List[Any]], List[Any]],
        decision_executor: Callable[[Session, List[Any]], None],
    ):
        self.session = session
        self.work_generator = work_generator
        self.event_generator = event_generator
        self.rule_evaluator = rule_evaluator
        self.decision_executor = decision_executor

    # -------------------------
    # Core Loop
    # -------------------------

    def tick(self) -> None:
        """
        Execute a single simulation tick.
        """

        # 1. Generate work
        new_work_items = self.work_generator(self.session)
        for work in new_work_items:
            self.session.add_work(work.work_id, work)

        # 2. Generate events
        events = self.event_generator(self.session)
        for event in events:
            self.session.record_event(event)

        # 3. Evaluate rules → decisions
        decisions = self.rule_evaluator(self.session, events)
        for decision in decisions:
            self.session.record_decision(decision)

        # 4. Apply decisions
        self.decision_executor(self.session, decisions)

        # 5. Advance time
        self.session.advance_time()

    # -------------------------
    # Run helpers
    # -------------------------

    def run(self, ticks: int) -> None:
        """
        Run multiple simulation ticks.
        """
        for _ in range(ticks):
            self.tick()