"""
Data Analyst Scenario — B2B SaaS CRM Analytics

Orchestrates learning phases and progression.
"""

from industries.tech.data_analyst.phases import phase1_foundations


class DataAnalystScenario:
    """
    Controls phase progression and exposes tasks
    to the simulation engine.
    """

    def __init__(self):
        self.phases = [
            phase1_foundations,
        ]

    # -------------------------
    # Initialization
    # -------------------------

    def initialize_session(self, session):
        """
        Prepare session flags and state.
        """

        session.flags.setdefault("scenario_phase", 0)
        session.flags.setdefault("scenario_complete", False)

    # -------------------------
    # Active Phase
    # -------------------------

    def _current_phase(self, session):
        index = session.flags.get("scenario_phase", 0)

        if index >= len(self.phases):
            return None

        return self.phases[index]

    # -------------------------
    # Task Exposure
    # -------------------------

    def get_available_tasks(self, session):
        """
        Returns tasks for the active phase.
        """

        phase = self._current_phase(session)

        if not phase:
            return []

        return phase.get_tasks()

    # -------------------------
    # Progress Evaluation
    # -------------------------

    def evaluate_progress(self, session):
        """
        Checks if current phase is complete
        and advances scenario.
        """

        phase = self._current_phase(session)

        if not phase:
            return

        if phase.is_complete(session):

            # Build artifact
            artifact = phase.build_portfolio_artifact(session)

            session.evidence.add_record(
                category="portfolio",
                reference="phase_artifact",
                note=str(artifact),
            )

            # Advance phase
            session.flags["scenario_phase"] += 1

            # Check completion
            if session.flags["scenario_phase"] >= len(self.phases):
                session.flags["scenario_complete"] = True

    # -------------------------
    # Completion Check
    # -------------------------

    def is_complete(self, session):
        return session.flags.get("scenario_complete", False)