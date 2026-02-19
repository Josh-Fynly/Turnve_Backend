"""
Simulation API Controller (Persistent)

Uses database-backed session storage.
"""

from core_engine.engine import SimulationEngine
from core_engine.session import Session

from database.models import init_db
from database.session_store import (
    save_session,
    load_session,
)

# Initialize DB tables on import
init_db()


# -------------------------
# Session Rehydration
# -------------------------

def _rehydrate_session(session_id: int):
    """
    Load session from DB and restore engine state.
    """

    record = load_session(session_id)

    if not record:
        return None, None

    engine = SimulationEngine(record["industry"])

    session = engine.create_session(record["role"])

    session.id = session_id
    session.restore(record["state"])

    return engine, session


# -------------------------
# Create Session
# -------------------------

def create_simulation(industry: str, role: str):

    engine = SimulationEngine(industry)
    session = engine.create_session(role)

    # Persist immediately
    save_session(session)

    return {
        "session_id": session.id,
        "industry": industry,
        "role": role,
    }


# -------------------------
# Step Simulation
# -------------------------

def step_simulation(session_id: int):

    engine, session = _rehydrate_session(session_id)

    if not session:
        return {"error": "Invalid session"}

    engine.step(session)

    save_session(session)

    return {
        "time": session.current_time(),
        "decisions": session.decisions,
        "events": session.events,
    }


# -------------------------
# Submit Task
# -------------------------

def submit_task(
    session_id: int,
    task_id: str,
    payload: dict,
):

    engine, session = _rehydrate_session(session_id)

    if not session:
        return {"error": "Invalid session"}

    scenario = session.flags.get("scenario")

    if not scenario:
        return {"error": "Scenario not initialized"}

    result = scenario.submit(
        session,
        task_id,
        payload,
    )

    save_session(session)

    return result


# -------------------------
# Get Portfolio
# -------------------------

def get_portfolio(session_id: int):

    engine, session = _rehydrate_session(session_id)

    if not session:
        return {"error": "Invalid session"}

    scenario = session.flags.get("scenario")

    if not scenario:
        return {"error": "Scenario not initialized"}

    return scenario.build_portfolio(session)


# -------------------------
# Export Portfolio PDF
# -------------------------

def export_portfolio_pdf(session_id: int):

    engine, session = _rehydrate_session(session_id)

    if not session:
        return {"error": "Invalid session"}

    scenario = session.flags.get("scenario")

    if not scenario:
        return {"error": "Scenario not initialized"}

    filepath = scenario.export_pdf(session)

    save_session(session)

    return {
        "status": "success",
        "file": filepath,
    }


# -------------------------
# End Simulation
# -------------------------

def end_simulation(session_id: int):

    engine, session = _rehydrate_session(session_id)

    if not session:
        return {"error": "Invalid session"}

    # Optional: mark complete
    session.flags["scenario_complete"] = True

    save_session(session)

    return {"status": "ended"}