"""
Tech industry integration layer.

Bridges:
- Generic Tech work engine
- Role-specific simulation scenarios
"""

from .work_generator import generate_tech_work
from industries.tech.data_analyst.scenario import DataAnalystScenario


# -------------------------
# Scenario Registry
# -------------------------

SCENARIOS = {
    "data analyst": DataAnalystScenario,
    "data_analyst": DataAnalystScenario,
}


def _initialize_scenario(session):
    role_key = session.role.lower()

    scenario_class = SCENARIOS.get(role_key)

    if not scenario_class:
        return None

    if not hasattr(session, "_scenario_instance"):
        session._scenario_instance = scenario_class()
        session._scenario_instance.initialize_session(session)

    return session._scenario_instance


# -------------------------
# Engine Hook
# -------------------------

def generate_initial_work(session):
    """
    Called once by the engine at session start.

    1. Initialize role scenario (if available)
    2. Register generic tech work canvas
    """

    # ---- Scenario layer ----
    _initialize_scenario(session)

    # ---- Existing work system ----
    work_items = generate_tech_work(session)

    for work in work_items:
        session.register_work(
            work_id=work.id,
            payload={
                "id": work.id,
                "title": work.title,
                "description": work.description,
                "estimated_effort": work.estimated_effort,
                "required_resources": work.required_resources,
                "priority": work.priority,
                "created_at": work.created_at,
                "status": work.status,
            },
        )