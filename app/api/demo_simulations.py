import uuid
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.services.simulation_engine import (
    load_simulation,
    initialize_state,
    apply_action,
    generate_score,
    generate_coach_summary,
)

router = APIRouter(prefix="/demo/simulations", tags=["Demo Simulations"])

# In-memory session store (demo only)
DEMO_SESSIONS: Dict[str, Dict[str, Any]] = {}


@router.post("/start")
def start_simulation(simulation_id: str):
    """
    Start a new demo simulation session.
    """
    try:
        scenario = load_simulation(simulation_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Simulation not found")

    session_id = str(uuid.uuid4())

    DEMO_SESSIONS[session_id] = {
        "scenario": scenario,
        "state": initialize_state(scenario),
        "history": [],
    }

    return {
        "session_id": session_id,
        "meta": scenario.get("meta", {}),
        "initial_state": DEMO_SESSIONS[session_id]["state"],
        "actions": scenario.get("actions", {}),
    }


@router.post("/act")
def take_action(
    session_id: str,
    action_id: str,
    choice: str,
):
    """
    Apply a decision to the simulation.
    """
    session = DEMO_SESSIONS.get(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        new_state, feedback, log = apply_action(
            scenario=session["scenario"],
            state=session["state"],
            action_id=action_id,
            choice=choice,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    session["state"] = new_state
    session["history"].append(log)

    return {
        "state": new_state,
        "feedback": feedback,
        "history": session["history"],
    }


@router.get("/score/{session_id}")
def get_score(session_id: str):
    """
    Get score and AI coach feedback.
    """
    session = DEMO_SESSIONS.get(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    score = generate_score(session["state"])
    summary = generate_coach_summary(session["state"], score)

    return {
        "score": score,
        "coach_feedback": summary,
    }