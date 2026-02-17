"""
Portfolio Artifact Registry

Collects artifacts from completed phases.
"""

from typing import Dict

from industries.tech.data_analyst.phases import phase1_foundations


# -------------------------
# Artifact Builders
# -------------------------

PHASE_ARTIFACTS = {
    0: phase1_foundations.build_portfolio_artifact,
}


# -------------------------
# Aggregation
# -------------------------

def collect_artifacts(session) -> Dict:
    """
    Gather artifacts from completed phases.
    """

    artifacts = []

    for phase_index, builder in PHASE_ARTIFACTS.items():

        if phase_index <= session.flags.get("scenario_phase", 0):

            artifact = builder(session)

            if artifact:
                artifacts.append(artifact)

    return {
        "role": session.role,
        "industry": session.industry,
        "artifacts": artifacts,
  }
