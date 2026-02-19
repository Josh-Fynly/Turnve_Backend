"""
Phase 1 — CRM Dataset Exploration

Learners analyze a synthetic B2B SaaS dataset
and compute core business metrics.
"""

from dataclasses import dataclass
from typing import List, Dict


# -------------------------
# Task Model
# -------------------------

@dataclass
class PhaseTask:
    id: str
    title: str
    description: str
    expected_output: Dict


# -------------------------
# Tasks
# -------------------------

def get_tasks() -> List[PhaseTask]:

    return [

        PhaseTask(
            id="p1_company_summary",
            title="Company distribution summary",
            description=(
                "Compute total number of companies and "
                "distribution by industry."
            ),
            expected_output={
                "total_companies": int,
                "industry_distribution": dict,
            },
        ),

        PhaseTask(
            id="p1_subscription_metrics",
            title="Subscription performance metrics",
            description=(
                "Calculate number of active vs churned subscriptions "
                "and average monthly revenue."
            ),
            expected_output={
                "active_subscriptions": int,
                "churned_subscriptions": int,
                "average_monthly_price": float,
            },
        ),

        PhaseTask(
            id="p1_engagement_analysis",
            title="Customer engagement analysis",
            description=(
                "Compute average logins and feature usage per company."
            ),
            expected_output={
                "average_logins": float,
                "average_feature_usage": float,
            },
        ),
    ]


# -------------------------
# Helpers
# -------------------------

def _validate_schema(expected: Dict, submission: Dict) -> bool:

    for key, expected_type in expected.items():

        if key not in submission:
            return False

        if not isinstance(submission[key], expected_type):
            return False

    return True


# -------------------------
# Evaluation
# -------------------------

def evaluate_task(session, task_id: str, submission: Dict) -> bool:

    tasks = {t.id: t for t in get_tasks()}

    task = tasks.get(task_id)

    if not task:
        return False

    if not _validate_schema(task.expected_output, submission):
        return False

    completed = session.flags.setdefault(
        "phase1_completed_tasks",
        set(),
    )

    completed.add(task_id)

    return True


# -------------------------
# Completion
# -------------------------

def is_complete(session) -> bool:

    completed = session.flags.get(
        "phase1_completed_tasks",
        set(),
    )

    return len(completed) == len(get_tasks())


# -------------------------
# Portfolio Artifact
# -------------------------

def build_portfolio_artifact(session) -> Dict:

    dataset = session.flags.get("dataset", {})

    return {
        "title": "CRM Analytics Diagnostic Report",
        "dataset_size": {
            "companies": len(dataset.get("companies", [])),
            "subscriptions": len(dataset.get("subscriptions", [])),
            "activity_records": len(dataset.get("activity", [])),
        },
        "skills_demonstrated": [
            "Business metric analysis",
            "Data aggregation",
            "Exploratory analytics",
        ],
    }