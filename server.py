"""
Turnve FastAPI Server

Exposes simulation endpoints over HTTP.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

from api.simulation import (
    create_simulation,
    step_simulation,
    submit_task,
    end_simulation,
    get_portfolio,
    export_portfolio_pdf,
)


# -------------------------
# App Initialization
# -------------------------

app = FastAPI(
    title="Turnve Simulation API",
    version="0.1.0",
)


# -------------------------
# Request Models
# -------------------------

class CreateSimulationRequest(BaseModel):
    industry: str
    role: str


class SubmitTaskRequest(BaseModel):
    session_id: int
    task_id: str
    payload: Dict


class SessionRequest(BaseModel):
    session_id: int


# -------------------------
# Routes
# -------------------------

@app.post("/simulation/start")
def start_simulation(req: CreateSimulationRequest):

    result = create_simulation(
        req.industry,
        req.role,
    )

    return result


@app.post("/simulation/step")
def step(req: SessionRequest):

    result = step_simulation(req.session_id)

    if "error" in result:
        raise HTTPException(400, result["error"])

    return result


@app.post("/simulation/submit")
def submit(req: SubmitTaskRequest):

    result = submit_task(
        req.session_id,
        req.task_id,
        req.payload,
    )

    if "error" in result:
        raise HTTPException(400, result["error"])

    return result


@app.post("/simulation/portfolio")
def portfolio(req: SessionRequest):

    result = get_portfolio(req.session_id)

    if "error" in result:
        raise HTTPException(400, result["error"])

    return result


@app.post("/simulation/export")
def export(req: SessionRequest):

    result = export_portfolio_pdf(req.session_id)

    if "error" in result:
        raise HTTPException(400, result["error"])

    return result


@app.post("/simulation/end")
def end(req: SessionRequest):

    result = end_simulation(req.session_id)

    if "error" in result:
        raise HTTPException(400, result["error"])

    return result


# -------------------------
# Health Check
# -------------------------

@app.get("/health")
def health():

    return {"status": "ok"}
