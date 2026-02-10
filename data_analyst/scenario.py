"""
Data Analyst Scenario Orchestrator

Coordinates multi-phase progression for the
B2B CRM SaaS Data Analyst simulation.

This module is the bridge between:

SimulationEngine ↔ Data Analyst Phases
"""

from typing import Dict, Any, List

from industries.tech.data_analyst.phases.phase1_foundations import (
    Phase1Foundations,
)


# -------------------------
# Scenario Metadata
# -------------------------

SCENARIO_ID = "tech_data_analyst_crm"

SCENARIO_INFO = {
    "title": "B2B CRM SaaS Analytics Simulation",
    "role": "Data Analyst",
    "company": "TurnveCRM",
    "description": (
        "You are a junior data analyst at a B2B CRM SaaS company. "
        "Your mission is to analyze customer, sales, and revenue data "
        "to support business decisions."
    ),
}


# -------------------------
# Phase Registry
# -------------------------

class PhaseRegistry:
    """
    Holds all simulation phases.

    Later phases can be added without
    modifying the engine interface.
    """

    def __init__(self):
        self._phases = [
            Phase1Foundations(),
            # Phase2Metrics(),
            # Phase3Experimentation(),
            # Phase4Reporting(),
        ]

    def get_phase(self, index: int):
        if index < 0 or index >= len(self._phases):
            return None
        return self._phases[index]

    def total_phases(self) -> int:
        return len(self._phases)


# -------------------------
# Scenario Controller
# -------------------------

class DataAnalystScenario:
    """
    Main orchestrator used by the SimulationEngine.
    """

    def __init__(self):
        self.registry = PhaseRegistry()

    # ---- Session Integration ----

    def initialize_session(self, session) -> None:
        """
        Attach scenario state to the session.
        """

        if not hasattr(session, "scenario_state"):
            session.scenario_state = {
                "current_phase": 0,
                "completed_phases": [],
                "portfolio_artifacts": [],
            }

    # ---- Phase Access ----

    def get_current_phase(self, session):
        index = session.scenario_state["current_phase"]
        return self.registry.get_phase(index)

    def get_available_tasks(self, session) -> List[Any]:
        phase = self.get_current_phase(session)
        if not phase:
            return []
        return phase.get_tasks()

    # ---- Submission Pipeline ----

    def submit_phase_work(
        self,
        session,
        submission: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Evaluate learner submission and advance scenario.
        """

        phase = self.get_current_phase(session)

        if not phase:
            return {
                "status": "completed",
                "message": "All phases finished",
            }

        result = phase.evaluate(submission)

        if result["passed"]:
            artifact = phase.build_portfolio_artifact(submission)

            session.scenario_state["portfolio_artifacts"].append(
                artifact
            )

            session.scenario_state["completed_phases"].append(
                session.scenario_state["current_phase"]
            )

            session.scenario_state["current_phase"] += 1

            return {
                "status": "phase_passed",
                "next_phase": session.scenario_state["current_phase"],
                "artifact_added": artifact["title"],
                "evaluation": result,
            }

        return {
            "status": "retry_required",
            "evaluation": result,
        }

    # ---- Scenario Status ----

    def is_complete(self, session) -> bool:
        return (
            session.scenario_state["current_phase"]
            >= self.registry.total_phases()
        )

    def get_portfolio(self, session) -> List[Dict[str, Any]]:
        return session.scenario_state["portfolio_artifacts"]
