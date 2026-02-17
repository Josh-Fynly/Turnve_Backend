"""
Portfolio Builder

Assembles learner portfolio from simulation artifacts.
"""

from typing import Dict

from industries.tech.data_analyst.portfolio.artifacts import (
    collect_artifacts,
)


# -------------------------
# Build Portfolio
# -------------------------

def build_portfolio(session) -> Dict:
    """
    Create structured portfolio record.
    """

    portfolio = collect_artifacts(session)

    portfolio["summary"] = {
        "completed_phases": session.flags.get(
            "scenario_phase",
            0,
        ),
        "status": "in_progress"
        if not session.flags.get("scenario_complete")
        else "completed",
    }

    # Store in session
    session.flags["portfolio"] = portfolio

    return portfolio