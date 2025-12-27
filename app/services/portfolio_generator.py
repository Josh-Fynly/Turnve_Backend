from typing import Dict, Any
from datetime import datetime


def generate_portfolio_artifact(
    user_id: str,
    simulation_id: str,
    scenario: Dict[str, Any],
    final_state: Dict[str, Any],
    score: Dict[str, Any],
    decision_log: list,
) -> Dict[str, Any]:
    """
    Generate a demo-ready portfolio artifact from a completed simulation.
    """

    meta = scenario.get("meta", {})

    skills_validated = []

    # Simple skill inference (rule-based for MVP)
    if final_state.get("risk", 1) < 0.4:
        skills_validated.append("Risk assessment")

    if final_state.get("stakeholder_trust", 0) > 0.6:
        skills_validated.append("Stakeholder communication")

    if abs(final_state.get("deadline_days", 0)) <= 2:
        skills_validated.append("Delivery tradeoff analysis")

    return {
        "user_id": user_id,
        "simulation_id": simulation_id,
        "project_title": meta.get(
            "title", "Professional Simulation Project"
        ),
        "industry": meta.get("industry"),
        "role": meta.get("role"),
        "decisions_made": decision_log,
        "final_score": score.get("overall"),
        "skills_validated": skills_validated,
        "coach_summary": f"Overall performance score: {score.get('overall')}",
        "completed_at": datetime.utcnow().isoformat() + "Z",
        "shareable": True,
    }