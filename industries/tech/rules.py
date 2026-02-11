"""
Tech Industry Rules Pipeline

Combines:
- Scenario-driven role tasks
- Generic tech work fallback
"""

from typing import List, Any

from industries.tech import _initialize_scenario
from industries.tech.work_generator import generate_tech_work


# -------------------------
# Scenario → Decision Bridge
# -------------------------

def _scenario_decisions(session) -> List[Any]:
    """
    Pull tasks from role scenario and convert
    them into engine decisions.
    """

    scenario = _initialize_scenario(session)

    if not scenario:
        return []

    tasks = scenario.get_available_tasks(session)

    decisions = []

    for task in tasks:
        decisions.append(
            {
                "decision_id": f"scenario_{task.id}",
                "title": task.title,
                "description": task.description,
            }
        )

    return decisions


# -------------------------
# Generic Tech Decisions
# -------------------------

def _generic_decisions(session) -> List[Any]:
    """
    Fallback to generic tech work.
    """

    work_items = generate_tech_work(session)

    decisions = []

    for work in work_items:
        decisions.append(
            {
                "decision_id": f"work_{work.id}",
                "title": work.title,
                "description": work.description,
            }
        )

    return decisions


# -------------------------
# Engine Hook
# -------------------------

def evaluate_rules(session) -> List[Any]:
    """
    Called by SimulationEngine every step.

    Flow:
    1. Pull scenario decisions
    2. Evaluate scenario progress
    3. Fallback to generic work if needed
    """

    scenario = _initialize_scenario(session)

    # ---- Scenario decisions ----
    if scenario:
        decisions = _scenario_decisions(session)

        # IMPORTANT: evaluate progress AFTER tasks are exposed
        scenario.evaluate_progress(session)

        if decisions:
            return decisions

    # ---- Fallback ----
    return _generic_decisions(session)