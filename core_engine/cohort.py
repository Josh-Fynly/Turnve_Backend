"""
Cohort Classification Engine

Maps onboarding scores to simulation tiers.
"""

from dataclasses import dataclass


@dataclass
class CohortProfile:
    score: int
    tier: str
    simulation_track: str


class CohortClassifier:

    FOUNDATION_MAX = 10
    APPLIED_MAX = 20

    @staticmethod
    def classify(score: int) -> CohortProfile:

        if score <= CohortClassifier.FOUNDATION_MAX:
            return CohortProfile(
                score=score,
                tier="foundation",
                simulation_track="guided_learning"
            )

        if score <= CohortClassifier.APPLIED_MAX:
            return CohortProfile(
                score=score,
                tier="applied",
                simulation_track="project_simulation"
            )

        return CohortProfile(
            score=score,
            tier="advanced",
            simulation_track="production_simulation"
        )