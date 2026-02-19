"""
Data Analyst Rules Pipeline
"""

from typing import List, Any

from industries.tech.data_analyst.scenario import DataAnalystScenario


# -------------------------
# Scenario singleton
# -------------------------

def _initialize_scenario(session):
    if "scenario" not in session.flags:
        scenario = DataAnalystScenario()
        scenario.initialize_session(session)
        session.flags["scenario"] = scenario

    return session.flags["scenario"]


# -------------------------
# Engine Hook
# -------------------------

def evaluate_rules(session) -> List[Any]:
    """
    Main entry point for Data Analyst simulation.
    """

    scenario = _initialize_scenario(session)

    tasks = scenario.get_available_tasks(session)

    decisions = []

    for task in tasks:
        decisions.append(
            {
                "decision_id": f"task_{task.id}",
                "title": task.title,
                "description": task.description,
            }
        )

    # Progress evaluation
    scenario.evaluate_progress(session)

    return decisions