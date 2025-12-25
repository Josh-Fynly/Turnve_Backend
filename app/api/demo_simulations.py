"""
Demo Simulation API
Used ONLY for MVP demos, frontend walkthroughs, and pitch videos.
Stateless + in-memory by design.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import uuid

from app.services.simulation_engine import (
    load_simulation,
    apply_action,
    generate_score,
    generate_coach_summary,
)

router = APIRouter(
    prefix="/api/v1/demo-simulations",
    tags=["Demo Simulations"],
)

# In-memory demo session store (RESET ON SERVER RESTART)
_DEMO_STATE: Dict[str, Dict[str, Any]] = {}


@router.post("/start")
def start_demo_simulation(simulation_id: str):
    """
    Start a demo simulation using a JSON scenario.
    """
    try:
        scenario = load_simulation(simulation_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Simulation not found")

    session_id = str(uuid.uuid4())

    _DEMO_STATE[session_id] = {
        "state": scenario["initial_state"],
        "meta": scenario.get("meta", {}),
    }

    return {
        "session_id": session_id,
        "meta": scenario.get("meta", {}),
        "state": scenario["initial_state"],
    }


@router.post("/{session_id}/action")
def apply_demo_action(
    session_id: str,
    action_id: str,
    choice: str,
):
    """
    Apply an action choice to the demo simulation.
    """
    if session_id not in _DEMO_STATE:
        raise HTTPException(status_code=404, detail="Session not found")

    session = _DEMO_STATE[session_id]

    new_state, feedback, audit = apply_action(
        state=session["state"],
        action_id=action_id,
        choice=choice,
    )

    session["state"] = new_state

    return {
        "state": new_state,
        "feedback": feedback,
        "decision": audit,
    }


@router.get("/{session_id}/score")
def get_demo_score(session_id: str):
    """
    Get final score + AI coach summary.
    """
    if session_id not in _DEMO_STATE:
        raise HTTPException(status_code=404, detail="Session not found")

    state = _DEMO_STATE[session_id]["state"]

    score = generate_score(state)
    coach_summary = generate_coach_summary(state, score)

    return {
        "score": score,
        "coach_summary": coach_summary,
  }
