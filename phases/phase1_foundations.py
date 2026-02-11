"""
Phase 1 — Foundations of B2B SaaS CRM Analytics

Goal:
Introduce learners to real-world SaaS datasets and
basic analytical thinking.

This phase builds:
- data exploration skills
- cleaning workflows
- business metric literacy
"""

from dataclasses import dataclass
from typing import List


# -------------------------
# Task Model
# -------------------------

@dataclass
class PhaseTask:
    id: str
    title: str
    description: str


# -------------------------
# Phase 1 Tasks
# -------------------------

def get_tasks() -> List[PhaseTask]:
    """
    Returns Phase 1 learning tasks.
    """

    return [
        PhaseTask(
            id="p1_load_dataset",
            title="Load CRM dataset",
            description=(
                "Import the provided B2B CRM dataset and inspect its structure. "
                "Identify key columns such as customer_id, signup_date, plan_type, "
                "revenue, and churn_status."
            ),
        ),
        PhaseTask(
            id="p1_clean_data",
            title="Clean missing and inconsistent data",
            description=(
                "Detect missing values, duplicates, and formatting issues. "
                "Apply cleaning techniques and document assumptions."
            ),
        ),
        PhaseTask(
            id="p1_explore_metrics",
            title="Explore core SaaS metrics",
            description=(
                "Compute descriptive statistics and summarize key SaaS metrics "
                "such as active customers, churn rate, and revenue distribution."
            ),
        ),
        PhaseTask(
            id="p1_generate_insights",
            title="Generate initial business insights",
            description=(
                "Write a short analysis explaining patterns in customer behavior "
                "and possible business implications."
            ),
        ),
    ]


# -------------------------
# Completion Logic
# -------------------------

def is_complete(session) -> bool:
    """
    Phase is complete when all tasks are marked finished.
    """

    completed = session.flags.get("phase1_completed_tasks", set())

    return len(completed) >= len(get_tasks())


# -------------------------
# Task Evaluation
# -------------------------

def evaluate_task(session, task_id: str, submission: dict) -> bool:
    """
    Evaluates learner submission.

    For MVP:
    Accept structured submission and mark complete.
    """

    completed = session.flags.setdefault(
        "phase1_completed_tasks",
        set(),
    )

    completed.add(task_id)

    return True


# -------------------------
# Portfolio Artifact
# -------------------------

def build_portfolio_artifact(session) -> dict:
    """
    Generates Phase 1 portfolio artifact.

    This will later be converted into PDF.
    """

    return {
        "title": "CRM Dataset Exploration Report",
        "summary": (
            "Analyzed B2B SaaS CRM dataset to identify "
            "customer behavior patterns and revenue trends."
        ),
        "skills_demonstrated": [
            "Data cleaning",
            "Exploratory data analysis",
            "Business metric interpretation",
        ],
    }