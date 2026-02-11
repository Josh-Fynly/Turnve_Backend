"""
Phase 1 — Data Familiarization & SQL Foundations

This module simulates onboarding analysis inside a B2B SaaS CRM company.

Responsibilities:
- Define tasks
- Validate learner outputs
- Emit simulation events
- Produce portfolio artifacts
"""

from dataclasses import dataclass
from typing import Dict, List, Any


# -------------------------
# Task Definitions
# -------------------------

@dataclass(frozen=True)
class PhaseTask:
    id: str
    title: str
    description: str
    required_outputs: List[str]


PHASE1_TASKS: List[PhaseTask] = [
    PhaseTask(
        id="schema_exploration",
        title="Dataset Exploration",
        description=(
            "Inspect CRM schema, identify relationships, and explain table structure."
        ),
        required_outputs=[
            "schema_explanation",
            "er_diagram",
        ],
    ),
    PhaseTask(
        id="customer_segmentation",
        title="Customer Segmentation Analysis",
        description=(
            "Analyze customer distribution by industry, geography, and signup trends."
        ),
        required_outputs=[
            "segmentation_sql",
            "segmentation_summary",
            "segmentation_charts",
        ],
    ),
    PhaseTask(
        id="user_activity_metrics",
        title="User Activity Metrics",
        description=(
            "Compute DAU and activity usage patterns across companies."
        ),
        required_outputs=[
            "activity_sql",
            "activity_report",
        ],
    ),
]


# -------------------------
# Evaluation Model
# -------------------------

class Phase1Evaluation:
    """
    Lightweight scoring model.

    Real version can later integrate:
    - SQL correctness checks
    - rubric scoring
    - ML-assisted grading
    """

    def score_submission(self, submission: Dict[str, Any]) -> Dict[str, Any]:
        score = 0
        feedback = []

        for task in PHASE1_TASKS:
            missing = [
                item for item in task.required_outputs
                if item not in submission
            ]

            if missing:
                feedback.append(
                    f"Task '{task.id}' missing outputs: {missing}"
                )
            else:
                score += 1

        completion_ratio = score / len(PHASE1_TASKS)

        return {
            "score": completion_ratio,
            "passed": completion_ratio >= 0.7,
            "feedback": feedback,
        }


# -------------------------
# Portfolio Artifact Builder
# -------------------------

class Phase1PortfolioBuilder:
    """
    Converts learner outputs into a structured artifact
    for the portfolio hub.
    """

    def build_artifact(self, submission: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": "Customer & Usage Overview Report",
            "phase": "phase1_foundations",
            "sections": {
                "schema_analysis": submission.get("schema_explanation"),
                "segmentation": submission.get("segmentation_summary"),
                "activity_metrics": submission.get("activity_report"),
            },
        }


# -------------------------
# Phase Controller
# -------------------------

class Phase1Foundations:
    """
    Entry point used by the SimulationEngine.
    """

    def __init__(self):
        self.tasks = PHASE1_TASKS
        self.evaluator = Phase1Evaluation()
        self.portfolio_builder = Phase1PortfolioBuilder()

    # ---- Simulation Interface ----

    def get_tasks(self) -> List[PhaseTask]:
        return self.tasks

    def evaluate(self, submission: Dict[str, Any]) -> Dict[str, Any]:
        return self.evaluator.score_submission(submission)

    def build_portfolio_artifact(
        self,
        submission: Dict[str, Any],
    ) -> Dict[str, Any]:
        return self.portfolio_builder.build_artifact(submission)
