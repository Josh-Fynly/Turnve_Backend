"""
Data Analyst Submission Interface

Handles learner task submissions and evaluation routing.
"""

from typing import Dict

from industries.tech.data_analyst.phases import phase1_foundations


# -------------------------
# Phase Registry
# -------------------------

PHASE_REGISTRY = {
    0: phase1_foundations,
}


# -------------------------
# Submission Entry Point
# -------------------------

def submit_task(
    session,
    task_id: str,
    submission: Dict,
) -> Dict:
    """
    Main submission interface.

    Routes submission to the active phase.
    """

    phase_index = session.flags.get("scenario_phase", 0)

    phase = PHASE_REGISTRY.get(phase_index)

    if not phase:
        return {
            "success": False,
            "error": "Invalid phase",
        }

    success = phase.evaluate_task(
        session,
        task_id,
        submission,
    )

    if not success:
        return {
            "success": False,
            "error": "Evaluation failed",
        }

    # Record evidence (optional MVP logging)
    session.record_event(
        {
            "type": "task_submission",
            "task_id": task_id,
        }
    )

    return {
        "success": True,
        "task_id": task_id,
        "phase": phase_index,
    }
