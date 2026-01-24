"""
Simulation Engine

Central orchestration layer for Turnve simulations.
Controls time, work generation, rules evaluation, and events.
"""

from typing import List

from core_engine.exceptions import EngineError
from core_engine.event import Event
from core_engine.decision import DecisionRule
from core_engine.evidence import EvidenceLog


class SimulationEngine:
    def __init__(
        self,
        session,
        work_generator,
        rules: List[DecisionRule] | None = None,
        events: List[Event] | None = None,
    ):
        self.session = session
        self.work_generator = work_generator
        self.rules = rules or []
        self.events = events or []

    # -------------------------
    # Engine Tick
    # -------------------------

    def tick(self):
        """
        Advance the simulation by one time unit.
        """

        try:
            self._advance_time()
            self._generate_work()
            self._apply_rules()
            self._trigger_events()
        except Exception as exc:
            raise EngineError(f"Engine tick failed: {exc}") from exc

    # -------------------------
    # Time
    # -------------------------

    def _advance_time(self):
        self.session.current_time += 1
        self.session.log(
            EvidenceLog.system(
                f"Time advanced to {self.session.current_time}"
            )
        )

    # -------------------------
    # Work Generation
    # -------------------------

    def _generate_work(self):
        new_work = self.work_generator(self.session)

        for item in new_work:
            self.session.add_work(item)
            self.session.log(
                EvidenceLog.work_created(item)
            )

    # -------------------------
    # Rules Evaluation
    # -------------------------

    def _apply_rules(self):
        for rule in self.rules:
            if rule.applies(self.session):
                decision = rule.evaluate(self.session)
                if decision:
                    self.session.apply_decision(decision)
                    self.session.log(
                        EvidenceLog.decision(decision)
                    )

    # -------------------------
    # Events
    # -------------------------

    def _trigger_events(self):
        for event in self.events:
            if event.should_trigger(self.session):
                event.trigger(self.session)
                self.session.log(
                    EvidenceLog.event(event)
                )

    # -------------------------
    # Run Loop
    # -------------------------

    def run(self, ticks: int):
        """
        Run the simulation for N ticks.
        """
        for _ in range(ticks):
            self.tick()