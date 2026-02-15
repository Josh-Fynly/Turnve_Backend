"""
Simulation API Layer

Exposes endpoints for:
- session creation
- task listing
- task execution
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from core_engine.engine import SimulationEngine
from industries.tech.data_analyst.phases import phase1_foundations

router = APIRouter(prefix="/simulation", tags=["simulation"])


# -------------------------
# In-memory session store (MVP)
# -------------------------

ACTIVE_SESSIONS = {}


# -------------------------
# Request Models
# -------------------------

class SessionCreateRequest(BaseModel):
    industry: str
    role: str


class TaskExecuteRequest(BaseModel):
    session_id: str
    task_id: str


# -------------------------
# Session Endpoints
# -------------------------

@router.post("/create")
def create_session(req: SessionCreateRequest):
    engine = SimulationEngine(req.industry)

    session = engine.create_session(req.role)

    session_id = str(id(session))

    ACTIVE_SESSIONS[session_id] = {
        "engine": engine,
        "session": session,
    }

    return {
        "session_id": session_id,
        "industry": req.industry,
        "role": req.role,
    }


# -------------------------
# Task Listing
# -------------------------

@router.get("/tasks/{session_id}")
def list_tasks(session_id: str):
    record = ACTIVE_SESSIONS.get(session_id)

    if not record:
        raise HTTPException(404, "Session not found")

    engine = record["engine"]
    session = record["session"]

    engine.step(session)

    return {
        "tasks": session.decisions,
        "time": session.current_time(),
    }


# -------------------------
# Task Execution
# -------------------------

@router.post("/execute")
def execute_task(req: TaskExecuteRequest):
    record = ACTIVE_SESSIONS.get(req.session_id)

    if not record:
        raise HTTPException(404, "Session not found")

    session = record["session"]

    try:
        result = phase1_foundations.evaluate_task(
            session,
            req.task_id,
        )

        return {
            "task_id": req.task_id,
            "result": result,
            "completed_tasks": list(
                session.flags.get("phase1_completed_tasks", [])
            ),
        }

    except Exception as e:
        raise HTTPException(400, str(e))
